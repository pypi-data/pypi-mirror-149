from django.conf import settings


__all__ = [
    "SETTING_PREFIX", "get_setting_name", "get_setting"
]


SETTING_PREFIX = "TWILIO_2FA_"


def get_setting_name(name):
    return f"{SETTING_PREFIX}{name.upper()}"


def get_setting(name, default=None, callback_kwargs=None):
    if not name.upper().startswith(SETTING_PREFIX):
        name = get_setting_name(name)

    if not hasattr(settings, name):
        return default

    value = getattr(settings, name)

    must_be_callable = True if name.endswith("_CB") else False

    if callable(value):
        if not callback_kwargs:
            callback_kwargs = {}

        return value(**callback_kwargs)
    elif must_be_callable and not callable(value):
        raise ValueError(f"Setting {name} must be callable")

    return value
