import os

from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from temba.tests import TembaTest

from temba.channels.models import Channel
from temba.contacts.models import EXTERNAL_SCHEME

from .type import PushinhoType


class PushinhoTypeTest(TembaTest):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_create_pushinho_channel(self):
        url = reverse("channels.types.pushinho.claim")

        self.login(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))

        self.assertContains(response, url)

        # try to claim a channel
        Channel.objects.all().delete()
        response = self.client.get(url)
        post_data = response.context["form"].initial

        main_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_one.png"), "rb")
        chat_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_two.png"), "rb")

        post_data["channel_name"] = "The New Channel"
        post_data["main_icon"] = SimpleUploadedFile(main_icon.name, main_icon.read())
        post_data["main_icon_color"] = "#18fae2"
        post_data["chat_icon"] = SimpleUploadedFile(chat_icon.name, chat_icon.read())
        post_data["chat_icon_color"] = "#a40aee"
        post_data["chat_push_message_color"] = "#23a519"
        post_data["chat_push_text_color"] = "#dbf609"
        post_data["chat_user_text_color"] = "#e2e0f0"
        post_data["auto_open"] = True
        post_data["keyword"] = "welcome_keyword"
        post_data["welcome_message"] = "Welcome to a Channel"

        response = self.client.post(url, post_data)
        pushinho_channel = Channel.objects.get()

        self.assertEqual(pushinho_channel.name, "The New Channel")
        self.assertFalse(pushinho_channel.country)
        self.assertEqual(pushinho_channel.org, self.user.get_org())
        self.assertEqual(pushinho_channel.address, "The New Channel")
        self.assertEqual(pushinho_channel.channel_type, PushinhoType.code)
        self.assertEqual(pushinho_channel.role, Channel.ROLE_SEND + Channel.ROLE_RECEIVE)
        self.assertEqual(pushinho_channel.schemes, [EXTERNAL_SCHEME])
        self.assertTrue(pushinho_channel.config)
        self.assertEqual(pushinho_channel.config.get("send_url"), settings.PUSH_WEB_SOCKET_URL)

        config_url = reverse("pushinho_configuration", args=[pushinho_channel.uuid])
        self.assertRedirect(response, config_url)

        response = self.client.get(config_url)
        self.assertEqual(200, response.status_code)

    def test_update_pushinho_channel(self):
        # Create the object using the view
        url = reverse("channels.types.pushinho.claim")

        self.login(self.admin)

        Channel.objects.all().delete()
        response = self.client.get(url)
        post_data = response.context["form"].initial

        main_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_one.png"), "rb")
        chat_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_two.png"), "rb")

        post_data["channel_name"] = "The New Channel"
        post_data["main_icon"] = SimpleUploadedFile(main_icon.name, main_icon.read())
        post_data["main_icon_color"] = "#18fae2"
        post_data["chat_icon"] = SimpleUploadedFile(chat_icon.name, chat_icon.read())
        post_data["chat_icon_color"] = "#a40aee"
        post_data["chat_push_message_color"] = "#23a519"
        post_data["chat_push_text_color"] = "#dbf609"
        post_data["chat_user_text_color"] = "#e2e0f0"
        post_data["auto_open"] = True
        post_data["keyword"] = "welcome_keyword"
        post_data["welcome_message"] = "Welcome to a Channel"

        response = self.client.post(url, post_data)
        pushinho_channel = Channel.objects.get()

        # Get informations the object with view for update
        update_url = reverse("channels.channel_update", args=[pushinho_channel.id])
        response = self.client.get(update_url)

        post_data_initial = response.context["form"].initial

        self.assertEqual(post_data_initial.get("name"), pushinho_channel.name)
        self.assertEqual(post_data_initial.get("config").get("main_icon_color"), "#18fae2")
        self.assertEqual(post_data_initial.get("config").get("chat_icon_color"), "#a40aee")
        self.assertEqual(post_data_initial.get("config").get("chat_push_message_color"), "#23a519")
        self.assertEqual(post_data_initial.get("config").get("chat_push_text_color"), "#dbf609")
        self.assertEqual(post_data_initial.get("config").get("chat_user_text_color"), "#e2e0f0")
        self.assertEqual(post_data_initial.get("config").get("auto_open"), 'true')
        self.assertEqual(post_data_initial.get("config").get("welcome_button"), "welcome_keyword")
        self.assertEqual(post_data_initial.get("config").get("welcome_message"), "Welcome to a Channel")

        # Update a object with view for update
        post_data["main_icon"] = None
        post_data["chat_icon"] = None
        post_data["channel_name"] = "Pushinho Channel"
        post_data["main_icon_color"] = "#DCDCDC"
        post_data["chat_user_text_color"] = "#800080"
        post_data["auto_open"] = False
        post_data["keyword"] = "keyword"

        response = self.client.post(update_url, post_data)

        channel_updated = Channel.objects.get()

        self.assertEqual(channel_updated.config.get("main_icon_color"), "#DCDCDC")
        self.assertEqual(channel_updated.name, "Pushinho Channel")
        self.assertEqual(channel_updated.config.get("chat_user_text_color"), "#800080")
        self.assertEqual(channel_updated.config.get("auto_open"), "false")
        self.assertEqual(channel_updated.config.get("welcome_button"), "keyword")

    def test_create_a_channel_with_welcome_message_and_without_keyword(self):
        url = reverse("channels.types.pushinho.claim")

        self.login(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))

        self.assertContains(response, url)

        # try to claim a channel
        Channel.objects.all().delete()
        response = self.client.get(url)
        post_data = response.context["form"].initial

        main_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_one.png"), "rb")
        chat_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_two.png"), "rb")

        post_data["channel_name"] = "The New Channel"
        post_data["main_icon"] = SimpleUploadedFile(main_icon.name, main_icon.read())
        post_data["main_icon_color"] = "#18fae2"
        post_data["chat_icon"] = SimpleUploadedFile(chat_icon.name, chat_icon.read())
        post_data["chat_icon_color"] = "#a40aee"
        post_data["chat_push_message_color"] = "#23a519"
        post_data["chat_push_text_color"] = "#dbf609"
        post_data["chat_user_text_color"] = "#e2e0f0"
        post_data["auto_open"] = True
        post_data["welcome_message"] = "Welcome to a Channel"

        response = self.client.post(url, post_data)
        self.assertTrue(response.context.get('form').errors)

    def test_configuration_pushinho_channel(self):
        url = reverse("channels.types.pushinho.claim")

        self.login(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))

        self.assertContains(response, url)

        # try to claim a channel
        Channel.objects.all().delete()
        response = self.client.get(url)
        post_data = response.context["form"].initial

        main_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_one.png"), "rb")
        chat_icon = open(os.path.join(self.BASE_DIR, "pushinho/test_files/profile_two.png"), "rb")

        post_data["channel_name"] = "The New Channel"
        post_data["main_icon"] = SimpleUploadedFile(main_icon.name, main_icon.read())
        post_data["main_icon_color"] = "#18fae2"
        post_data["chat_icon"] = SimpleUploadedFile(chat_icon.name, chat_icon.read())
        post_data["chat_icon_color"] = "#a40aee"
        post_data["chat_push_message_color"] = "#23a519"
        post_data["chat_push_text_color"] = "#dbf609"
        post_data["chat_user_text_color"] = "#e2e0f0"
        post_data["auto_open"] = True
        post_data["keyword"] = "welcome_keyword"
        post_data["welcome_message"] = "Welcome to a Channel"

        response = self.client.post(url, post_data)
        channel_updated = Channel.objects.get()

        response = self.client.get(reverse("pushinho_configuration", args=[channel_updated.uuid]))
        self.assertEqual(response.status_code, 200)


class UploadFileToAWS(TembaTest):

    def test_upload_file_to_aws(self):
        pass
