from django.urls import path
from . import views

app_name = 'events_app'

urlpatterns = [
    path('', views.index, name='index'),
]
