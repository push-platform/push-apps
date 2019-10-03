from django import forms

from django.utils.translation import ugettext_lazy as _

from colorful.widgets import ColorFieldWidget

from temba.channels.views import UpdateChannelForm
from temba.channels.models import Channel
from temba.channels.views import ClaimViewMixin

from .utils import (
    CHANNEL_NAME,
    MAIN_ICON,
    CHAT_ICON,
    MAIN_ICON_COLOR,
    MAIN_ICON_URL,
    CHAT_ICON_COLOR,
    CHAT_ICON_URL,
    CHAT_PUSH_MESSAGE_COLOR,
    CHAT_PUSH_TEXT_COLOR,
    CHAT_USER_TEXT_COLOR,
    AUTO_OPEN,
    WELCOME_BUTTON,
    WELCOME_MESSAGE,
    upload_icon_to_aws,
    create_config
)


class PushinhoForm(forms.Form):
    channel_name = forms.CharField(max_length=40)

    main_icon = forms.ImageField(required=True)
    main_icon_color = forms.CharField(
        max_length=7, help_text=_("Hexa Decimal Color"), widget=ColorFieldWidget()
    )

    chat_icon = forms.ImageField(required=True)
    chat_icon_color = forms.CharField(
        max_length=7, help_text=_("Hexa Decimal Color"), widget=ColorFieldWidget()
    )
    chat_push_message_color = forms.CharField(
        max_length=7, help_text=_("Hexa Decimal Color"), widget=ColorFieldWidget()
    )
    chat_push_text_color = forms.CharField(
        max_length=7, help_text=_("Hexa Decimal Color"), widget=ColorFieldWidget()
    )
    chat_user_text_color = forms.CharField(
        max_length=7, help_text=_("Hexa Decimal Color"), widget=ColorFieldWidget()
    )

    auto_open = forms.BooleanField(required=False)
    welcome_button = forms.CharField(required=False)
    welcome_message = forms.CharField(required=False)

    def clean(self):
        if self.data.get(WELCOME_MESSAGE) and not self.data.get(WELCOME_BUTTON):
            raise forms.ValidationError(
                _("You cannot add a Welcome Message without a Keyword")
            )


class PushinhoFormCreate(PushinhoForm, ClaimViewMixin.Form):
    pass


class PushinhoFormUpdate(PushinhoForm, UpdateChannelForm):
    def add_config_fields(self):
        self.fields[MAIN_ICON].required = False
        self.fields[CHAT_ICON].required = False

        self.fields[CHANNEL_NAME].initial = self.object.name
        self.fields[MAIN_ICON_COLOR].initial = self.object.config[MAIN_ICON_COLOR]
        self.fields[CHAT_ICON_COLOR].initial = self.object.config[CHAT_ICON_COLOR]
        self.fields[CHAT_PUSH_MESSAGE_COLOR].initial = self.object.config[
            CHAT_PUSH_MESSAGE_COLOR
        ]
        self.fields[CHAT_PUSH_TEXT_COLOR].initial = self.object.config[
            CHAT_PUSH_TEXT_COLOR
        ]
        self.fields[CHAT_USER_TEXT_COLOR].initial = self.object.config[
            CHAT_USER_TEXT_COLOR
        ]
        self.fields[AUTO_OPEN].initial = self.object.config[AUTO_OPEN]
        self.fields[WELCOME_BUTTON].initial = self.object.config[WELCOME_BUTTON]
        self.fields[WELCOME_MESSAGE].initial = self.object.config[WELCOME_MESSAGE]

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

        main_icon_url = self[MAIN_ICON].value()
        chat_icon_url = self[CHAT_ICON].value()

        if not main_icon_url:
            main_icon_url = instance.config.get(MAIN_ICON_URL)
        else:
            main_icon_url = upload_icon_to_aws(main_icon_url)

        if not chat_icon_url:
            chat_icon_url = instance.config.get(CHAT_ICON_URL)
        else:
            chat_icon_url = upload_icon_to_aws(chat_icon_url)

        config = create_config(
            main_icon_url=main_icon_url, chat_icon_url=chat_icon_url, data=data
        )

        instance.name = data[CHANNEL_NAME]
        instance.config = config
        return super().save(commit)
