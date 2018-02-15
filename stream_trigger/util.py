import os
import error


def get_env_var(env_var, default=None):
    result = os.environ.get(env_var, default)
    if result is None:
        raise error.MissingEnvironmentValue("{} environment variable must be set.".format(env_var))
    if not result:
        raise error.InvalidHostnameError()
    return result
