from django.urls import path

from . import views


urlpatterns = [
    # Urls for Informative Flow
    path(
        "channels/channel/configuration/<uuid>/",
        views.ChannelConfiguration.as_view(),
        name="pushinho_configuration",
    )
]
