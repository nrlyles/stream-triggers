import os
import json
import requests

from stream_trigger import error
from base import BaseBulb


class PhilipsHueBulb(BaseBulb):

    def __init__(self, name):
        BaseBulb.__init__(self, name)
        self._bridge_ip = self.__get_env_var("HUE_BRIDGE_HOSTNAME")
        self._username = self.__get_env_var("HUE_BRIDGE_USERNAME")

    def set_off(self):
        self.__set_state(False)

    def set_on(self):
        self.__set_state(True)

    def set_color(self, color):
        raise error.UnsupportedAction("Action set_color is not allowed for this light type.")

    def __get_env_var(self, env_var):
        result = os.environ.get(env_var)
        if result is None:
            raise error.MissingEnvironmentValue("{} environment variable must be set.".format(env_var))
        if not result:
            raise error.InvalidHostnameError()
        return result

    def _check_error(self, json_response):
        desc_to_except = {
            "unauthorized user": error.InvalidUserError("User {} is not an authorized user.".format(self._username))
        }
        for item in json_response:
            if isinstance(item, dict) and item.get("error") is not None:
                error_desc = item["error"]["description"]
                raise desc_to_except[error_desc] if error_desc in desc_to_except \
                    else error.UnknownError("An unknown error has occured.")

    def _request_with_error_check(self, **kwargs):
        response = requests.request(**kwargs)
        self._check_error(response.json())
        return response.json()

    def _is_found(self):
        return self.name in self._request_with_error_check(
            method="GET", url="http://{}/api/{}/lights".format(self._bridge_ip, self._username))

    def __set_state(self, is_on):
        if self._is_found():
            self._request_with_error_check(method="PUT",
                                            url="http://{}/api/{}/lights/{}/state".format(
                                                self._bridge_ip, self._username, self.name),
                                            data=json.dumps({"on": is_on})
                                            )
        else:
            raise error.InvalidLightError("Could not find light: {}".format(self.name))