from django.conf import settings
from django.core.exceptions import ValidationError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from .conf import *


__all__ = [
    "get_twilio_client", "verify_phone_number", "parse_phone_number",
]


default_region = get_setting(
    "PHONE_NUMBER_DEFAULT_REGION",
    default="US"
)


def get_twilio_client(**kwargs):
    if "account_sid" not in kwargs:
        kwargs["account_sid"] = get_setting("ACCOUNT_SID")
        kwargs["auth_token"] = get_setting("AUTH_TOKEN")

    args = [
        kwargs.pop("account_sid"),
        kwargs.pop("auth_token"),
    ]

    return TwilioClient(*args, **kwargs)


def parse_phone_number(phone_number):
    try:
        return phonenumbers.parse(phone_number, default_region)
    except NumberParseException as e:
        raise ValidationError(str(e))


def verify_phone_number(phone_number, do_lookup=False):
    allowed_country_codes = get_setting(
        "PHONE_NUMBER_ALLOWED_COUNTRIES",
        default=["US"]
    )

    disallowed_country_codes = get_setting(
        "PHONE_NUMBER_DISALLOWED_COUNTRIES",
        default=[]
    )

    do_lookup_setting = get_setting(
        "PHONE_NUMBER_CARRIER_LOOKUP",
        default=True
    )

    allowed_carrier_types = get_setting(
        "PHONE_NUMBER_ALLOWED_CARRIER_TYPES",
        default=["mobile"]
    )

    if do_lookup and not do_lookup_setting:
        do_lookup = False

    phone_number = parse_phone_number(phone_number)

    if not phonenumbers.is_valid_number(phone_number):
        raise ValidationError("Invalid phone number")

    if do_lookup:
        try:
            response = (get_twilio_client().lookups
                .phone_numbers(phone_number.national_number)
                .fetch(type=["carrier"])
            )
        except TwilioRestException as e:
            raise ValidationError("Unable to valid your phone number at this time. Please try again later.")

        country_code = response.country_code
        carrier_type = response.carrier.get("type", "")

        if carrier_type not in allowed_carrier_types:
            raise ValidationError(f"{carrier_type.title()} phone numbers are not allowed. "
                                  f"Must be a {' or '.join(allowed_carrier_types)} phone number.")

        if country_code not in allowed_country_codes or country_code in disallowed_country_codes:
            raise ValidationError(f"We do not allow phone numbers originating from {country_code}.")

    return True
