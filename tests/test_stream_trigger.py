import mock

from stream_trigger import stream_trigger


@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulbColor')
@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulb')
@mock.patch('stream_trigger.stream_trigger.time')
def test_follower(mock_time, mock_bulb, mock_bulb_color):
    bulb_instance = mock.MagicMock()
    color_bulb_instance = mock.MagicMock()
    mock_bulb.return_value = bulb_instance
    mock_bulb_color.return_value = color_bulb_instance
    stream_trigger.alert()
    assert bulb_instance.set_off.call_count == 1
    assert bulb_instance.set_on.call_count == 1
    assert color_bulb_instance.set_off.call_count == 1
    assert color_bulb_instance.set_color.call_count == 11


@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulbColor')
@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulb')
@mock.patch('stream_trigger.stream_trigger.time')
def test_on_message_insufficient_bits(mock_time, mock_bulb, mock_bulb_color):
    bulb_instance = mock.MagicMock()
    color_bulb_instance = mock.MagicMock()
    mock_bulb.return_value = bulb_instance
    mock_bulb_color.return_value = color_bulb_instance
    message = """{
        "event": "EVENT_CHEER",
        "data": {
            "bits": 5
        }
    }"""
    stream_trigger.on_message(None, message)
    assert bulb_instance.set_off.call_count == 0
    assert bulb_instance.set_on.call_count == 0
    assert color_bulb_instance.set_off.call_count == 0
    assert color_bulb_instance.set_color.call_count == 0


@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulbColor')
@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulb')
@mock.patch('stream_trigger.stream_trigger.time')
def test_on_message_enough_bits(mock_time, mock_bulb, mock_bulb_color):
    bulb_instance = mock.MagicMock()
    color_bulb_instance = mock.MagicMock()
    mock_bulb.return_value = bulb_instance
    mock_bulb_color.return_value = color_bulb_instance
    message = """{
        "event": "EVENT_CHEER",
        "data": {
            "bits": 100
        }
    }"""
    stream_trigger.on_message(None, message)
    assert bulb_instance.set_off.call_count == 1
    assert bulb_instance.set_on.call_count == 1
    assert color_bulb_instance.set_off.call_count == 1
    assert color_bulb_instance.set_color.call_count == 11


@mock.patch('stream_trigger.stream_trigger.time')
def test_on_open(mock_time):
    stream_trigger.api_key = "test_key"
    ws_mock = mock.MagicMock()
    stream_trigger.on_open(ws_mock)
    ws_mock.send.called_once_with({
        "author": "stream_trigger_user",
        "website": "twitch.tv",
        "api_key": "test_key",
        "events": [
            "EVENT_SUB",
            "EVENT_FOLLOW",
            "EVENT_HOST",
            "EVENT_CHEER"
        ]
    })
