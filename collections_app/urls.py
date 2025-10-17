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
    
    # ============================================================================
    # BASKET URL PATTERNS - Shopping cart functionality
    # ============================================================================
    
    # View shopping basket
    path('basket/', views.basket_view, name='basket'),
    
    # Add artwork to basket - supporting both old and new IDs
    path('basket/add/<int:artwork_id>/', views.add_to_basket, name='add_to_basket'),
    path('basket/add_artwork/<int:artwork_id>/', views.add_to_basket, name='add_artwork_to_basket'),
    
    # Update basket item quantity
    path('basket/update/<int:item_id>/', views.update_basket_item, name='update_basket_item'),
    
    # Remove item from basket
    path('basket/remove/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    
    # Clear entire basket
    path('basket/clear/', views.clear_basket, name='clear_basket'),
    
    # Get basket count (AJAX)
    path('basket/count/', views.get_basket_count, name='basket_count'),
    
    # ============================================================================
    # CHECKOUT URL PATTERNS - Order processing and payment
    # ============================================================================
    
    # Checkout page with order summary and billing form
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    
    # User dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
