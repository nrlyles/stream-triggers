#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import mock
import pytest
from stream_trigger.bulb.philipsbulb import PhilipsHueBulb
from stream_trigger import error

__author__ = "nlyles"
__copyright__ = "nlyles"
__license__ = "none"


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
def test_instantiate(mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "some_username"]
    test_bulb = PhilipsHueBulb("test")
    mock_environ.get.assert_has_calls([mock.call("HUE_BRIDGE_HOSTNAME"), mock.call("HUE_BRIDGE_USERNAME")])
    assert test_bulb._bridge_ip == "10.10.10.10"
    assert test_bulb._username == "some_username"


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
def test_instantiate_empty_ip(mock_environ):
    mock_environ.get.return_value = ""
    with pytest.raises(error.InvalidHostnameError):
        _ = PhilipsHueBulb("test")


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
def test_instantiate_missing(mock_environ):
    mock_environ.get.return_value = None
    with pytest.raises(error.MissingEnvironmentValue) as e:
        _ = PhilipsHueBulb("test")
        assert e.message == "HUE_BRIDGE_HOSTNAME environment variable must be set."


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_is_found(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "some_username"]
    mock_requests.request.side_effect = [MockResponse(json_data={"1": {"state": {}}}, status_code=200)]
    bulb = PhilipsHueBulb("1")
    assert bulb._is_found()
    mock_requests.request.assert_called_once_with("GET", url="http://10.10.10.10/api/some_username/lights")


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_is_found(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "some_username"]
    mock_requests.request.side_effect = [MockResponse(json_data={"1": {"state": {}}}, status_code=200)]
    bulb = PhilipsHueBulb("1")
    assert bulb._is_found()
    mock_requests.request.assert_called_once_with(method="GET", url="http://10.10.10.10/api/some_username/lights")


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_is_invalid_user(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "bad_username"]
    mock_requests.request.side_effect = [MockResponse(
        json_data=[{"error": {"description": "unauthorized user"}}],
        status_code=200
    )]
    bulb = PhilipsHueBulb("1")
    with pytest.raises(error.InvalidUserError):
        bulb._is_found()


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_unknown_error(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "username"]
    mock_requests.request.side_effect = [MockResponse(
        json_data=[{"error": {"description": "some unknown error"}}],
        status_code=200
    )]
    bulb = PhilipsHueBulb("1")
    with pytest.raises(error.UnknownError):
        bulb._is_found()


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_set_off(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "username"]
    mock_requests.request.side_effect = [
        MockResponse(
            json_data={"1": {"state": {}}},
            status_code=200
        ),
        MockResponse(
            json_data=[{"success": {"lights/1/state/on": True}}],
            status_code=200
        )
    ]
    bulb = PhilipsHueBulb("1")
    bulb.set_off()
    mock_requests.request.assert_has_calls([mock.call(method="GET", url="http://10.10.10.10/api/username/lights"),
                                            mock.call(method="PUT",
                                                      url="http://10.10.10.10/api/username/lights/1/state",
                                                      data=json.dumps({"on": False}))
                                            ])


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_set_off_not_found(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "some_username"]
    mock_requests.request.side_effect = [MockResponse(json_data={"1": {"state": {}}}, status_code=200)]
    bulb = PhilipsHueBulb("2")
    with pytest.raises(error.InvalidLightError):
        bulb.set_off()


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_set_off(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "username"]
    mock_requests.request.side_effect = [
        MockResponse(
            json_data={"1": {"state": {}}},
            status_code=200
        ),
        MockResponse(
            json_data=[{"success": {"lights/1/state/on": True}}],
            status_code=200
        )
    ]
    bulb = PhilipsHueBulb("1")
    bulb.set_on()
    mock_requests.request.assert_has_calls([mock.call(method="GET", url="http://10.10.10.10/api/username/lights"),
                                            mock.call(method="PUT",
                                                      url="http://10.10.10.10/api/username/lights/1/state",
                                                      data=json.dumps({"on": True}))
                                            ])


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_is_invalid_user(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "bad_username"]
    bulb = PhilipsHueBulb("1")
    with pytest.raises(error.UnsupportedAction):
        bulb.set_color("123456")
