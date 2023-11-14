import requests
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings

def get_joke():
    """Get a joke"""
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = response.json()["joke"]

    # if the joke do not have a punch line try it again and again
    # the punch line is the part after the question mark
    if "?" not in joke:
        return get_joke()

    # split the joke into question and answer
    question, answer = joke.split("?")
    return question, answer


class IndexView(TemplateView):
    """
    Index view
    Renders the index.html template with a joke context
    """

    """return joke.html if request header contains htmx"""
    def get_template_names(self):
        if self.request.headers.get("Hx-Request"):
            return ["joke.html"]
        else:
            return ["index.html"]

    def get_context_data(self, **kwargs):
        """Get the context"""
        context = super().get_context_data(**kwargs)
        context["question"], context["answer"] = get_joke()
        return context
