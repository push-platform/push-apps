from django.utils.translation import ugettext_lazy as _
from temba.contacts.models import (
    TEL_SCHEME,
    FACEBOOK_SCHEME,
    TWITTER_SCHEME,
    TWITTERID_SCHEME,
    VIBER_SCHEME,
    LINE_SCHEME,
    TELEGRAM_SCHEME,
    EMAIL_SCHEME,
    EXTERNAL_SCHEME,
    JIOCHAT_SCHEME,
    WECHAT_SCHEME,
    FCM_SCHEME,
    WHATSAPP_SCHEME,
)


URN_SCHEME_CONFIG = (
    (TEL_SCHEME, _("Phone number"), "tel_e164"),
    (FACEBOOK_SCHEME, _("Facebook identifier"), FACEBOOK_SCHEME),
    (TWITTER_SCHEME, _("Twitter handle"), TWITTER_SCHEME),
    (TWITTERID_SCHEME, _("Twitter ID"), TWITTERID_SCHEME),
    (VIBER_SCHEME, _("Viber identifier"), VIBER_SCHEME),
    (LINE_SCHEME, _("LINE identifier"), LINE_SCHEME),
    (TELEGRAM_SCHEME, _("Telegram identifier"), TELEGRAM_SCHEME),
    (EMAIL_SCHEME, _("Email address"), EMAIL_SCHEME),
    (EXTERNAL_SCHEME, _("External identifier"), EXTERNAL_SCHEME),
    (JIOCHAT_SCHEME, _("JioChat identifier"), JIOCHAT_SCHEME),
    (WECHAT_SCHEME, _("WeChat identifier"), WECHAT_SCHEME),
    (FCM_SCHEME, _("Firebase Cloud Messaging identifier"), FCM_SCHEME),
    (WHATSAPP_SCHEME, _("WhatsApp identifier"), WHATSAPP_SCHEME),
    ("ps", _("Pushinho identifier"), "ps"),
)
