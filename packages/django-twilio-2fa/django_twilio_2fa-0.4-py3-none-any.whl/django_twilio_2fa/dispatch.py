import django.dispatch


__all__ = [
    "twilio_2fa_verification_sent",
]


twilio_2fa_verification_sent = django.dispatch.Signal()
