from django.urls import path
from . import views

app_name = 'collections_app'

urlpatterns = [
    # Existing URL patterns for collections and art
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path(
        'collection/<int:pk>/', views.collection_detail, name='collection_detail'
    ),
    path('art/<int:pk>/', views.art_detail, name='art_detail'),
    
    # ============================================================================
    # NEW ARTWORK URL PATTERNS - Routes for displaying artwork price, size, medium
    # ============================================================================
    
    # Display list of all available artworks with price, size, and medium
    path('artworks/', views.artwork_list, name='artwork_list'),
    
    # Display detailed view of a specific artwork with all information
    path('artwork/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    
    # Display featured artworks on homepage or featured section
    path('artworks/featured/', views.featured_artworks, name='featured_artworks'),
    
    # Display all artworks by a specific artist
    path('artworks/artist/<int:artist_id>/', views.artworks_by_artist, name='artworks_by_artist'),
    
    # Search and filter artworks by price range
    path('artworks/search/price/', views.artwork_search_by_price, name='artwork_search_by_price'),
]
