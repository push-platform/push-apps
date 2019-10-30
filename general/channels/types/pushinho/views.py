from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from smartmin.views import SmartFormView

from temba.channels.models import Channel
from temba.channels.views import ClaimViewMixin

from .forms import PushinhoFormCreate
from .utils import (
    PUSHINHO_SCHEME,
    CHANNEL_NAME,
    MAIN_ICON,
    CHAT_ICON,
    upload_icon_to_aws,
    create_config
)


class PushinhoView(ClaimViewMixin, SmartFormView):

    form_class = PushinhoFormCreate

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        org = user.get_org()

        if not org:  # pragma: no cover
            raise Exception(_("No org for this user, cannot claim"))

        # Upload icons and get urls
        main_icon_url = upload_icon_to_aws(self.request.FILES.get(MAIN_ICON))
        chat_icon_url = upload_icon_to_aws(self.request.FILES.get(CHAT_ICON))

        # Get a config for Channel and Save on Model
        config = create_config(
            main_icon_url=main_icon_url, chat_icon_url=chat_icon_url, data=data
        )

        # Define a channel
        channel = self.request.GET.get("channel", None)
        if channel:  # pragma: needs cover
            # make sure they own it
            channel = self.request.user.get_org().channels.filter(pk=channel).first()

        # Define a role
        role = Channel.ROLE_SEND + Channel.ROLE_RECEIVE

        # Configure a External Channel
        self.object = Channel.add_config_external_channel(
            org=org,
            user=self.request.user,
            country=None,
            address=data[CHANNEL_NAME],
            channel_type=self.channel_type,
            config=config,
            role=role,
            schemes=[PUSHINHO_SCHEME],
            parent=channel,
        )

        return super(PushinhoView, self).form_valid(form)

    def get_success_url(self):
        if self.channel_type.show_config_page:
            return reverse("pushinho_configuration", args=[self.object.uuid])
        else:
            return reverse("pushinho_configuration", args=[self.object.uuid])
