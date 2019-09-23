from django.conf.urls import url
from django.urls import include

from temba.public.urls import urlpatterns

from .general.channels import urls as channel_urls

from .views import (
    IndexView,
)

urlpatterns += [
    url(r"^push/home$", IndexView.as_view(), {}, "push_app.public_index"),
    url(r"^push/", include(channel_urls), {}, "push_channels"),
]
