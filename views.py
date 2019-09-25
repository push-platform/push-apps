from urllib.parse import parse_qs
from smartmin.views import SmartTemplateView


class IndexView(SmartTemplateView):
    template_name = "public_index.haml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thanks"] = "thanks" in self.request.GET
        context["errors"] = "errors" in self.request.GET
        if context["errors"]:
            errors = parse_qs(context["url_params"][1:]).get("errors")
            if isinstance(errors, list) and len(errors) > 0:
                context["error_msg"] = errors[0]

        return context
