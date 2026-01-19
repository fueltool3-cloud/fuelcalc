from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.fuel_calculator, name='fuel_calculator'),
]