from django.contrib import admin
from django.urls import path
from django.urls import re_path
from .views.usermanagement import UserManagementAPI  
from django.http import HttpResponse

# Fungsi untuk menangani URL utama
def home_view(request):
    return HttpResponse("Welcome to the Django API! Go to /usermanagement/ for the User Management API.")

urlpatterns = [
    path('', home_view, name='home'),  # Route untuk halaman utama
    path('admin/', admin.site.urls),
  path('usermanagement/', UserManagementAPI.as_view(), name='user_management'),
    re_path(r'^usermanagement$', UserManagementAPI.as_view(), name='user_management_no_slash'),

]
