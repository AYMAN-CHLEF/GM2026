from django.urls import path
from django.views.generic import TemplateView

app_name = 'public'
urlpatterns = [path('', TemplateView.as_view(template_name='innovation_economy.html'), name='impact')]
