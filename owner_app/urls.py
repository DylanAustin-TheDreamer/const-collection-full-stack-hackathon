from django.urls import path
from . import views

app_name = 'owner_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('art/', views.art_list, name='art_list'),
    path('art/create/', views.create_art, name='create_art'),
    path('art/<int:pk>/edit/', views.edit_art, name='edit_art'),
    path('exhibitions/', views.exhibitions_list, name='exhibitions_list'),
    path(
        'exhibitions/create/',
        views.create_exhibition,
        name='create_exhibition',
    ),
    path(
        'exhibitions/<int:pk>/edit/',
        views.edit_exhibition,
        name='edit_exhibition',
    ),
    path(
        'exhibitions/<int:exhibition_pk>/assign-art/',
        views.assign_art,
        name='assign_art',
    ),
    path('about/edit/', views.edit_artist, name='edit_artist'),
    path('collections/', views.collections_list, name='collections_list'),
    path('collections/create/', views.create_collection, name='create_collection'),
    path('collections/<int:pk>/edit/', views.edit_collection, name='edit_collection'),
]
