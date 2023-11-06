from django.views.generic import TemplateView
from django.conf import settings


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return {"api_url": settings.API_URL}
