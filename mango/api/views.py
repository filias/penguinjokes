import requests
from django.http import HttpResponse
from django.views import View


class GetJokeView(View):
    def get(self, request, *args, **kwargs):
        """Get a joke"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        joke = response.json()["joke"]

        # Split the joke into question and answer
        if "?" in joke:
            split_joke = joke.split("?")
            question = f"{split_joke[0]} ?"
            answer = split_joke[1]
        else:
            answer = ""

        return HttpResponse(f'<div id="joke-1" class="text-xl font-medium text-black" hx-swap-oob="true">{question}<div>'
         f'<div id="joke-2" class="text-slate-500" hx-swap-oob="true">{answer}</div>')
