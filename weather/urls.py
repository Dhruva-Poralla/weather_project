from django.urls import path
from . import views

urlpatterns = [
    path('get-report/', views.get_weather, name='weather'),
]