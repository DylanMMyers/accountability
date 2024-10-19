from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_page, name='custom_page'),
]
