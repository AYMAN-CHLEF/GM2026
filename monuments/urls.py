from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.monument_tech_card, name='monument_detail'),
]