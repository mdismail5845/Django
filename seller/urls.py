from django.urls import path
from seller import views

urlpatterns = [
    path('seller_dashboard', views.seller_dashboard, name='seller_dashboard')
]
