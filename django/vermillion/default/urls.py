from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('service_definitions', views.ServiceDefinitionListView.as_view(), name='service_definitions'),
    path('container_templates', views.ContainerTemplateListView.as_view(), name='container_templates'),
]
