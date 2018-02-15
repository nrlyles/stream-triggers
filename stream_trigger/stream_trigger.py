import json
import time
import websocket

from .bulb.philipsbulb import PhilipsHueBulb
from .bulb.philipsbulbcolor import PhilipsHueBulbColor
from util import get_env_var

bulb1name = get_env_var("MAIN_LIGHT", "1")
bulb2name = get_env_var("COLOR_LIGHT", "2")
username = get_env_var("USERNAME", "stream_trigger_user")
website = get_env_var("WEBSITE", "twitch.tv")
api_key = get_env_var("STREAMLABS_API_KEY")
streamlabs_hostname = get_env_var("STREAMLABS_HOSTNAME", "localhost")
min_bits = get_env_var("MIN_BITS", 100)


def alert(timeout=10):
    bulb1 = PhilipsHueBulb(bulb1name)
    bulb2 = PhilipsHueBulbColor(bulb2name)
    colors = [65285, 46014, 55725, 24208]
    bulb1.set_off()
    t = 0
    while t <= timeout:
        bulb2.set_color(colors[t % len(colors)])
        t += 1
        time.sleep(1)

    bulb2.set_off()
    bulb1.set_on()


def on_message(ws, message):
    print message
    message_dict = json.loads(message)
    if message_dict.get("event") == "EVENT_CHEER":
        if message_dict.get("data").get("bits") < min_bits:
            return
    alert()


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("closed")


auth = {
    "author": username,
    "website": website,
    "api_key": api_key,
    "events": [
        "EVENT_SUB",
        "EVENT_FOLLOW",
        "EVENT_HOST",
        "EVENT_CHEER"
    ]
}


def on_open(ws):
    time.sleep(5)
    ws.send(json.dumps(auth))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://{}:3337/streamlabs".format(streamlabs_hostname),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
