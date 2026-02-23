from django.urls import path
from customer import views

urlpatterns = [
    path('customer_dashboard',views.customer_dashboard, name='customer_dashboard')
]
