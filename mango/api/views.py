import requests
from django.http import HttpResponse
from django.views import View


class GetJokeView(View):
    def get(self, request, *args, **kwargs):
        """Get a joke"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        joke = response.json()["joke"]
        return HttpResponse(joke)
