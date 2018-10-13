from django.urls import path
from . import views

urlpatterns = [
    path('api/stores', views.ListStores.as_view(), name='list_stores'),
]
