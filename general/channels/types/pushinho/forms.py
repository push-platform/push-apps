from django import forms

from django.utils.translation import ugettext_lazy as _

from colorful.widgets import ColorFieldWidget

from temba.channels.views import UpdateChannelForm
from temba.channels.models import Channel
from temba.channels.views import ClaimViewMixin

from .utils import upload_icon_to_aws, create_config


class PushinhoForm(forms.Form):
    channel_name = forms.CharField(max_length=40)

    main_icon = forms.ImageField(required=True)
    main_icon_color = forms.CharField(
        max_length=7,
        help_text=_('Hexa Decimal Colour'),
        widget=ColorFieldWidget())

    chat_icon = forms.ImageField(required=True)
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

    def clean(self):
        if self.data.get("welcome_message") and not self.data.get("keyword"):
            raise forms.ValidationError(_("You cannot add a Welcome Message without a Keyword"))


class PushinhoFormCreate(PushinhoForm, ClaimViewMixin.Form):
    pass


class PushinhoFormUpdate(PushinhoForm, UpdateChannelForm):

    def add_config_fields(self):
        self.fields["main_icon"].required = False
        self.fields["chat_icon"].required = False

        self.fields["channel_name"].initial = self.object.name
        self.fields["main_icon_color"].initial = self.object.config["main_icon_color"]
        self.fields["chat_icon_color"].initial = self.object.config["chat_icon_color"]
        self.fields["chat_push_message_color"].initial = self.object.config["chat_push_message_color"]
        self.fields["chat_push_text_color"].initial = self.object.config["chat_push_text_color"]
        self.fields["chat_user_text_color"].initial = self.object.config["chat_user_text_color"]
        self.fields["auto_open"].initial = self.object.config["auto_open"]
        self.fields["keyword"].initial = self.object.config["welcome_button"]
        self.fields["welcome_message"].initial = self.object.config["welcome_message"]

    class Meta:
        model = Channel
        fields = []
        config_fields = []
        readonly = []
        labels = {}
        helps = {}

    def save(self, commit=True):
        instance = super(PushinhoFormUpdate, self).save(commit=False)
        data = self.data

        main_icon_url = self['main_icon'].value()
        chat_icon_url = self['chat_icon'].value()

        if not main_icon_url:
            main_icon_url = instance.config.get("main_icon_url")
        else:
            main_icon_url = upload_icon_to_aws(main_icon_url)

        if not chat_icon_url:
            main_icon_url = instance.config.get("chat_icon_url")
        else:
            chat_icon_url = upload_icon_to_aws(chat_icon_url)

        config = create_config(
            main_icon_url=main_icon_url, chat_icon_url=chat_icon_url,
            data=data)

        instance.name = data["channel_name"]
        instance.config = config
        return super().save(commit)
