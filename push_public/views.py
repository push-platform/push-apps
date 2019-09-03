from urllib.parse import parse_qs, urlencode

from smartmin.views import SmartCreateView, SmartCRUDL, SmartFormView, SmartListView, SmartReadView, SmartTemplateView

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, View

from temba.apks.models import Apk
from temba.public.models import Lead, Video
from temba.utils import analytics, get_anonymous_user, json
from temba.utils.text import random_string


class IndexView(SmartTemplateView):
    template_name = "push/public_index.haml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thanks"] = "thanks" in self.request.GET
        context["errors"] = "errors" in self.request.GET
        if context["errors"]:
            errors = parse_qs(context["url_params"][1:]).get("errors")
            if isinstance(errors, list) and len(errors) > 0:
                context["error_msg"] = errors[0]

        return context