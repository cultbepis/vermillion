from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from . import models

from docker import from_env as docker_client
from docker.errors import DockerException

class IndexView(TemplateView):
    template_name = 'vermillion/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = models.Service.objects.all()
        paginator = Paginator(services, 5)
        page = self.request.GET.get("page", 1)
        try:
            show_services = paginator.page(page)
        except PageNotAnInteger:
            show_services = paginator.page(1)
        except EmptyPage:
            show_services = paginator.page(paginator.num_pages)

        context["services"] = show_services
        return context
