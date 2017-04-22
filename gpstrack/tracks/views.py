from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from config.settings.base import GOOGLE_API_KEY


class MapView(TemplateView, ContextMixin):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_key'] = GOOGLE_API_KEY
        return context


