from django.urls import path
from . import views

app_name = 'collections_app'

urlpatterns = [
    path('', views.index, name='index'),
]
