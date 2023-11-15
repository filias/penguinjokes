import requests
from django.views.generic import TemplateView


def get_joke():
    response = requests.get(
        "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
    )
    joke = response.json()["joke"]

    # if the joke does not have a punch line try it again and again
    # the punch line is the part after the question mark
    if "?" not in joke:
        return get_joke()

    # split the joke into question and answer
    question, answer = joke.split("?")
    return f"{question}?", answer


class IndexView(TemplateView):
    """
    Renders the index.html template with a joke context
    """

    def get_template_names(self):
        # Return joke.html if request header contains htmx
        if self.request.headers.get("Hx-Request"):
            return ["joke.html"]
        else:
            return ["index.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"], context["answer"] = get_joke()
        return context
