import boto3

from django.conf import settings

from temba.channels.models import Channel
from temba.utils.s3 import public_file_storage

CHANNEL_NAME = "channel_name"
MAIN_ICON = "main_icon"
MAIN_ICON_COLOR = "main_icon_color"
MAIN_ICON_URL = "main_icon_url"
CHAT_ICON = "chat_icon"
CHAT_ICON_COLOR = "chat_icon_color"
CHAT_ICON_URL = "chat_icon_url"
CHAT_PUSH_MESSAGE_COLOR = "chat_push_message_color"
CHAT_PUSH_TEXT_COLOR = "chat_push_text_color"
CHAT_USER_TEXT_COLOR = "chat_user_text_color"
KEYWORD = "keyword"
AUTO_OPEN = "auto_open"
WELCOME_BUTTON = "welcome_button"
WELCOME_MESSAGE = "welcome_message"


def upload_icon_to_aws(icon):
    # Initialize connection with AWS and Boto S3
    session = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.resource("s3")

    # Upload Icon to bucket on AWS
    main_icon = icon
    icon_path = settings.PUSHINHO_ICONS_AWS_PATH + icon.name
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=icon_path, Body=main_icon
    )
    icon_url = public_file_storage.url(icon_path)
    return icon_url


def create_config(main_icon_url, chat_icon_url, data):

    auto_open = str(data.get(AUTO_OPEN)).casefold()

    # Dict Config for save informations and show on HTML Returns
    config = {
        MAIN_ICON_URL: main_icon_url,
        MAIN_ICON_COLOR: data.get(MAIN_ICON_COLOR),
        CHAT_ICON_COLOR: data.get(CHAT_ICON_COLOR),
        CHAT_ICON_URL: chat_icon_url,
        CHAT_PUSH_MESSAGE_COLOR: data.get(CHAT_PUSH_MESSAGE_COLOR),
        CHAT_PUSH_TEXT_COLOR: data.get(CHAT_PUSH_TEXT_COLOR),
        CHAT_USER_TEXT_COLOR: data.get(CHAT_USER_TEXT_COLOR),
        AUTO_OPEN: auto_open,
        WELCOME_BUTTON: data.get("keyword"),
        WELCOME_MESSAGE: data.get(WELCOME_MESSAGE),
        Channel.CONFIG_SEND_URL: settings.PUSH_WEB_SOCKET_URL,
        Channel.CONFIG_SEND_METHOD: "POST",
        Channel.CONFIG_CONTENT_TYPE: Channel.CONTENT_TYPES.get("CONTENT_TYPE_JSON"),
        Channel.CONFIG_MAX_LENGTH: 640,
        Channel.CONFIG_ENCODING: Channel.ENCODING_DEFAULT,
    }

    return config
