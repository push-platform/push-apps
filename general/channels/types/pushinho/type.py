from django.utils.translation import ugettext_lazy as _

from temba.channels.models import ChannelType

from .views import PushinhoView


class PushinhoType(ChannelType):
    """
    The Pushinho channel
    """

    code = "PS"
    category = ChannelType.Category.API

    name = "Pushinho"
    configuration_urls = ""

    claim_blurb = _(
        """Connect to your website."""
    )
    claim_view = PushinhoView
