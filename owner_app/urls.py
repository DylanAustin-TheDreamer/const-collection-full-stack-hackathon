from django.urls import path
from . import views

app_name = 'owner_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('art/', views.art_list, name='art_list'),
    path('art/create/', views.create_art, name='create_art'),
    path('art/<int:pk>/edit/', views.edit_art, name='edit_art'),
    path(
        'art/<int:pk>/toggle-featured/',
        views.toggle_featured_art,
        name='toggle_featured_art',
    ),
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
    path(
        'exhibitions/<int:exhibition_pk>/assign-media/',
        views.assign_media,
        name='assign_media',
    ),
    path(
        'art/<int:pk>/delete/',
        views.delete_art,
        name='delete_art',
    ),
    path(
        'collections/<int:pk>/delete/',
        views.delete_collection,
        name='delete_collection',
    ),
    path(
        'exhibitions/<int:pk>/delete/',
        views.delete_exhibition,
        name='delete_exhibition',
    ),
    path('about/edit/', views.edit_artist, name='edit_artist'),
    path(
        'collections/',
        views.collections_list,
        name='collections_list',
    ),
    path(
        'collections/create/',
        views.create_collection,
        name='create_collection',
    ),
    path(
        'collections/<int:pk>/edit/',
        views.edit_collection,
        name='edit_collection',
    ),
]
