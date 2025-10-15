from django.urls import path
from . import views

app_name = 'owner_app'

urlpatterns = [
    path('', views.index, name='index'),
]
