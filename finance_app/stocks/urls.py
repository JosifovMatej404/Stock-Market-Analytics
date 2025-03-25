from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('company/<str:symbol>/', views.company_dashboard, name='company_dashboard'),
    path('company/<str:symbol>/regenerate/', views.regenerate_prediction, name='regenerate_prediction'),
]
