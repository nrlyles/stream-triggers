#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import mock
import pytest
from stream_trigger.bulb.philipsbulbcolor import PhilipsHueBulbColor
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
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_change_color(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "username"]
    bulb = PhilipsHueBulbColor("1")
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
    bulb.set_color(12345)
    mock_requests.request.assert_has_calls([mock.call(method="GET", url="http://10.10.10.10/api/username/lights"),
                                            mock.call(method="PUT",
                                                      url="http://10.10.10.10/api/username/lights/1/state",
                                                      data=json.dumps({"on": True, "hue": 12345}))
                                            ])


@mock.patch('stream_trigger.bulb.philipsbulb.os.environ')
@mock.patch('stream_trigger.bulb.philipsbulb.requests')
def test_change_color(mock_requests, mock_environ):
    mock_environ.get.side_effect = ["10.10.10.10", "username"]
    bulb = PhilipsHueBulbColor("2")
    with pytest.raises(error.InvalidLightError):
        bulb.set_color(12345)
