from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path('api/users/register', views.UserCreate.as_view(), name='register'),
    path('api/users/login', views.Login.as_view(), name='login'),
    path('api/users/logout', views.Logout.as_view(), name='logout'),
]