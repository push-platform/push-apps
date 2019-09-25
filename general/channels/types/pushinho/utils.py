import boto3

from django.conf import settings

from temba.channels.models import Channel
from temba.utils.s3 import public_file_storage


def upload_icon_to_aws(icon):
    # Initialize connection with AWS and Boto S3
    session = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.resource("s3")

    # Upload Icon to bucket on AWS
    main_icon = icon
    main_icon_path = settings.PUSHINHO_ICONS_AWS_PATH + main_icon.name
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=main_icon_path, Body=main_icon
    )
    icon_url = public_file_storage.url(main_icon_path)
    return icon_url


def create_config(main_icon_url, chat_icon_url, data):

    auto_open = str(data.get("auto_open")).casefold()

    # Dict Config for save informations and show on HTML Returns
    config = {
        "main_icon_url": main_icon_url,
        "main_icon_color": data.get("main_icon_color"),
        "chat_icon_color": data.get("chat_icon_color"),
        "chat_icon_url": chat_icon_url,
        "chat_push_message_color": data.get("chat_push_message_color"),
        "chat_push_text_color": data.get("chat_push_text_color"),
        "chat_user_text_color": data.get("chat_user_text_color"),
        "auto_open": auto_open,
        "welcome_button": data.get("keyword"),
        "welcome_message": data.get("welcome_message"),
        Channel.CONFIG_SEND_URL: settings.PUSH_WEB_SOCKET_URL,
        Channel.CONFIG_SEND_METHOD: "POST",
        Channel.CONFIG_CONTENT_TYPE: Channel.CONTENT_TYPES.get("CONTENT_TYPE_JSON"),
        Channel.CONFIG_MAX_LENGTH: 640,
        Channel.CONFIG_ENCODING: Channel.ENCODING_DEFAULT,
    }

    return config
