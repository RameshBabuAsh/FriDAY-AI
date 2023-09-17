from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('llmResponse', views.llmResponse, name='llmResponse'),
    path('parameter', views.parameter, name='parameter')
]