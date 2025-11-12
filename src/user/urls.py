from django.urls import path
from user.views.log_in import login_view
from user.views.client_view import dashboard_client
from user.views.admin_view import admin_dashboard
from user.views.super_admin_view import super_admin_dashboard
from user.views.create_account import create_account
from user.views.logout import logout_view



urlpatterns = [
    path('login/', login_view, name='login'),
    path('client-dashboard/', dashboard_client, name='client_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('super-admin-dashboard/', super_admin_dashboard, name='super_admin_dashboard'),
    path('create-account/',create_account,name='create_account'),
    path('logout/',logout_view, name= 'logout')
]