from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "home.html"


class ThanksPage(TemplateView):
    template_name = "index.html"

