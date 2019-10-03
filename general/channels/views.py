from smartmin.views import SmartReadView
from django.conf import settings

from temba.channels.models import Channel


class ChannelConfiguration(SmartReadView):
    model = Channel
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    template_name = "channels/pushinho_configuration.haml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = self.object.callback_domain
        context["ip_addresses"] = settings.IP_ADDRESSES

        # populate with our channel type
        channel_type = Channel.get_type_from_code(self.object.channel_type)
        context["configuration_template"] = channel_type.get_configuration_template(
            self.object
        )
        context["configuration_blurb"] = channel_type.get_configuration_blurb(
            self.object
        )
        context["configuration_urls"] = channel_type.get_configuration_urls(self.object)
        context["show_public_addresses"] = channel_type.show_public_addresses

        return context
