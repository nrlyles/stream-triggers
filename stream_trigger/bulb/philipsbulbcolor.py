from philipsbulb import PhilipsHueBulb
from stream_trigger import error

import json

class PhilipsHueBulbColor(PhilipsHueBulb):

    def __init__(self, name):
        PhilipsHueBulb.__init__(self, name)

    def set_color(self, color):
        if self._is_found():
            self._request_with_error_check(method="PUT",
                                            url="http://{}/api/{}/lights/{}/state".format(
                                                self._bridge_ip, self._username, self.name),
                                            data=json.dumps({"on": True, "hue": color})
                                            )
        else:
            raise error.InvalidLightError("Could not find light: {}".format(self.name))
