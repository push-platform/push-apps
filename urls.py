from django.conf.urls import url
from temba.public.urls import urlpatterns

from .views import (
    IndexView,
)

urlpatterns += [
    url(r"^push/$", IndexView.as_view(), {}, "push_app.public_index"),
]
