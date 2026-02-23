from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home,name='home'),
    path('register/', views.register,name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('resend_email/', views.resend_email, name='resend_email'),
    path('login/', views.login_view, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password,name='reset_password'),
    path('reset_password_confirm/<str:uidb64>/<str:token>/', views.reset_password_confirm,name='reset_password_confirm'),
    path('reset_password_done/', views.reset_password_done,name='reset_password_done'),
    path('account_details/', views.account_details,name='account_details'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]
