from django.urls import path

from .views import GetJokeView


urlpatterns = [
    path("jokes", GetJokeView.as_view(), name="jokes"),
]
app_name = "api"
