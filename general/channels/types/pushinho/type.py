from django.utils.translation import ugettext_lazy as _

from temba.channels.models import ChannelType

from .views import PushinhoView
from .forms import PushinhoFormUpdate


class PushinhoType(ChannelType):
    """
    The Pushinho channel
    """

    code = "PS"
    category = ChannelType.Category.API

    name = "Pushinho"

    claim_blurb = _("""Connect to your website.""")
    claim_view = PushinhoView
    extra_links = [
        dict(link=_("HTML For Pushinho Configuration to Integrate to your Website"), name="pushinho_configuration")
    ]
    update_form = PushinhoFormUpdate
