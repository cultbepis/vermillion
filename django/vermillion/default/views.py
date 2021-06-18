from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from . import models

from docker import from_env as docker_client
from docker.errors import DockerException

class IndexView(TemplateView):
    template_name = 'default/index.html'

class VermillionListView(ListView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_rows"] = len(context[self.context_object_name]) > 0
        return context

class ServiceView(VermillionListView):
    model = models.Service
    context_object_name = "services"
    paginate_by = 5

class ServiceDefinitionListView(VermillionListView):
    model = models.ServiceDefinition
    context_object_name = "service_definitions"

class ContainerTemplateListView(VermillionListView):
    model = models.ContainerTemplate
    context_object_name = "container_templates"
