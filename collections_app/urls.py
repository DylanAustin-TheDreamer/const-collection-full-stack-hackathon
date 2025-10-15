from django.urls import path
from . import views

app_name = 'collections_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path(
        'collection/<int:pk>/', views.collection_detail, name='collection_detail'
    ),
    path('art/<int:pk>/', views.art_detail, name='art_detail'),
]
