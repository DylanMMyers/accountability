# dj_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other paths
    path('process-input/', views.process_input, name='process_input'),  # Add this line
]
