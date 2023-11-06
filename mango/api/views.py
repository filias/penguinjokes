import requests
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework.views import APIView


class GetJokeView(APIView):
    def get(self, request, *args, **kwargs):
        """Get a joke"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        joke = response.json()["joke"]
        return HttpResponse(joke)
