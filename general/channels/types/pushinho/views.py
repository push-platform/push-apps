import boto3

from smartmin.views import SmartFormView

from django import forms
from django.utils.translation import ugettext_lazy as _

from temba.channels.models import Channel
from temba.channels.views import ClaimViewMixin
from temba.contacts.models import EXTERNAL_SCHEME

from colorful.widgets import ColorFieldWidget
from temba.utils.s3 import public_file_storage
from django.conf import settings


class PushinhoView(ClaimViewMixin, SmartFormView):
    class PushinhoClaimForm(ClaimViewMixin.Form):
        main_icon = forms.ImageField()
        main_icon_color = forms.CharField(
            max_length=7,
            help_text=_('Hexa Decimal Colour'),
            widget=ColorFieldWidget())

        chat_icon = forms.ImageField()
        chat_icon_color = forms.CharField(
            max_length=7,
            help_text=_('Hexa Decimal Colour'),
            widget=ColorFieldWidget())
        chat_push_message_color = forms.CharField(
            max_length=7,
            help_text=_('Hexa Decimal Colour'),
            widget=ColorFieldWidget())
        chat_push_text_color = forms.CharField(
            max_length=7,
            help_text=_('Hexa Decimal Colour'),
            widget=ColorFieldWidget())
        chat_user_text_color = forms.CharField(
            max_length=7,
            help_text=_('Hexa Decimal Colour'),
            widget=ColorFieldWidget())

        auto_open = forms.BooleanField(required=False)
        keyword = forms.CharField(required=False)
        welcome_message = forms.CharField(required=False)
        channel_name = forms.CharField(max_length=40)

        def clean(self):
            if self.data.get("welcome_message") and not self.data.get("keyword"):
                raise forms.ValidationError(_("You cannot add a Welcome Message without a Keyword"))

    form_class = PushinhoClaimForm

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        org = user.get_org()

        if not org:  # pragma: no cover
            raise Exception(_("No org for this user, cannot claim"))

        # Initialize connection with AWS and Boto S3
        session = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        s3 = session.resource('s3')

        # Upload MainIcon
        main_icon = self.request.FILES.get('main_icon')
        main_icon_path = settings.PUSHINHO_ICONS_AWS_PATH + main_icon.name
        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=main_icon_path, Body=main_icon)
        main_icon_url = public_file_storage.url(main_icon_path)

        # Upload ChatIcon
        chat_icon = self.request.FILES.get('chat_icon')
        chat_icon_path = settings.PUSHINHO_ICONS_AWS_PATH + chat_icon.name
        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=chat_icon_path, Body=chat_icon)
        chat_icon_url = public_file_storage.url(chat_icon_path)

        auto_open = str(data["auto_open"]).casefold()

        # Dict Config for save informations and show on HTML Returns
        config = {
            "main_icon_url": main_icon_url,
            "main_icon_color": data["main_icon_color"],
            "chat_icon_color": data["chat_icon_color"],
            "chat_icon_url": chat_icon_url,
            "chat_push_message_color": data["chat_push_message_color"],
            "chat_push_text_color": data["chat_push_text_color"],
            "chat_user_text_color": data["chat_user_text_color"],
            "auto_open": auto_open,
            "welcome_button": data["keyword"],
            "welcome_message": data["welcome_message"],
            Channel.CONFIG_SEND_URL: settings.PUSH_WEB_SOCKET_URL,
            Channel.CONFIG_SEND_METHOD: "POST",
            Channel.CONFIG_CONTENT_TYPE: Channel.CONTENT_TYPES.get("CONTENT_TYPE_JSON"),
            Channel.CONFIG_MAX_LENGTH: 640,
            Channel.CONFIG_ENCODING: Channel.ENCODING_DEFAULT,
        }

        # Define a channel
        channel = self.request.GET.get("channel", None)
        if channel:  # pragma: needs cover
            # make sure they own it
            channel = self.request.user.get_org().channels.filter(pk=channel).first()

        # Define a role
        role = Channel.ROLE_SEND + Channel.ROLE_RECEIVE

        # Configure a External Channel
        self.object = Channel.add_config_external_channel(
            org, self.request.user, None, data["channel_name"],
            self.channel_type, config, role, [EXTERNAL_SCHEME], parent=channel
        )

        return super(PushinhoView, self).form_valid(form)
