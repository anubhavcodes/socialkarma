import os

from sentry_sdk.utils import BadDsn

sentinel = object()


def get_environment_variable(key, default=sentinel, coerce=str):
    try:
        value = os.environ[key]
        return coerce(value)
    except KeyError:
        if default != sentinel:
            return default
        raise ValueError("You must specify '{}' environment variable.".format(key))
    except Exception as e:
        raise ValueError("Error while parsing environment variable '{}', more info: '{}'.".format(key, e))


def configure_sentry():
    sentry_dsn = get_environment_variable("SENTRY_DSN", str)
    if not sentry_dsn:
        return
    try:
        import sentry_sdk

        sentry_sdk.init(dsn=sentry_dsn)
    except BadDsn:
        raise BadDsn(f"Unable to init sentry with {sentry_dsn}")
