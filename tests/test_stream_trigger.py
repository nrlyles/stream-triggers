import mock

from stream_trigger import stream_trigger

@mock.patch('stream_trigger.stream_trigger.PhilipsHueBulb')
@mock.patch('stream_trigger.stream_trigger.time')
def test_follower(mock_time, mock_bulb):
    bulb_instance = mock.MagicMock()
    mock_bulb.return_value = bulb_instance
    stream_trigger.follower()
    bulb_instance.set_off.assert_called_once_with()
    bulb_instance.set_on.assert_called_once_with()
