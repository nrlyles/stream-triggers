import bottle
import time
from .bulb.philipsbulb import PhilipsHueBulb


@bottle.post('/follower')
def follower():
    bulb1 = PhilipsHueBulb("1")
    bulb1.set_off()
    time.sleep(5)
    bulb1.set_on()


if __name__ == "__main__":
    bottle.run(host="0.0.0.0")
