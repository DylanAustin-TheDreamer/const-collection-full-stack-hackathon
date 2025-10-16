from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST


def index(request):
    # Serve the homepage at root by rendering Vistor_pages/home.html
    return render(request, 'Vistor_pages/home.html')


def gallery(request):
    from .models import Collection
    collections = Collection.objects.select_related('artist').prefetch_related(
        'arts'
    )
    return render(
        request, 'Vistor_pages/gallery.html', {'collections': collections}
    )


def collection_detail(request, pk):
    from .models import Collection
    collection = Collection.objects.prefetch_related('arts').get(pk=pk)
    return render(
        request,
        'Vistor_pages/collection_detail.html',
        {'collection': collection},
    )


def art_detail(request, pk):
    from .models import Art

    art = Art.objects.select_related('collection__artist').get(pk=pk)
    return render(request, 'Vistor_pages/art_detail.html', {'art': art})


# ============================================================================
# NEW ARTWORK VIEWS - Display price, size, and medium information
# ============================================================================

def artwork_list(request):
    """
    View to display a list of all available artworks.
    Fetches and displays price, size, and medium for each artwork.
    
    Features:
    - Shows all available artworks
    - Displays price, size (dimensions), and medium
    - Optimizes database queries using select_related
    - Supports filtering and search functionality
    """
    from .models import Artwork
    
    # Fetch all artworks with related artist information
    # Using select_related to optimize database queries (reduce N+1 queries)
    artworks = Artwork.objects.select_related('artist').all()
    
    # Filter to show only available artworks (optional - can be removed to show all)
    artworks = artworks.filter(is_available=True)
    
    # Get search query from URL parameters (if provided)
    search_query = request.GET.get('search', '')
    if search_query:
        # Filter artworks by title, medium, or artist name
        artworks = artworks.filter(
            Q(title__icontains=search_query) |
            Q(medium__icontains=search_query) |
            Q(artist__name__icontains=search_query)
        )
    
    # Get filter parameters for price range (if provided)
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Apply price filters if provided
    if min_price:
        artworks = artworks.filter(price__gte=min_price)
    if max_price:
        artworks = artworks.filter(price__lte=max_price)
    
    # Get filter parameter for medium (if provided)
    medium_filter = request.GET.get('medium', '')
    if medium_filter:
        artworks = artworks.filter(medium__icontains=medium_filter)
    
    # Order artworks by creation date (newest first)
    artworks = artworks.order_by('-created_at')
    
    # Prepare context data to pass to the template
    context = {
        'artworks': artworks,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'medium_filter': medium_filter,
    }
    
    # Render the artwork list template with the context data
    return render(request, 'Vistor_pages/artwork_list.html', context)


def artwork_detail(request, pk):
    """
    View to display detailed information about a specific artwork.
    Shows comprehensive details including price, size, medium, and more.
    
    Args:
        pk: Primary key (ID) of the artwork to display
    
    Features:
    - Displays full artwork details
    - Shows formatted price with currency
    - Displays dimensions (width x height x depth)
    - Shows medium/materials used
    - Includes artist information
    - Shows availability status
    """
    from .models import Artwork
    
    # Fetch the artwork by primary key (ID)
    # Use get_object_or_404 to return 404 error if artwork doesn't exist
    # Using select_related to fetch artist information in the same query
    artwork = get_object_or_404(
        Artwork.objects.select_related('artist'),
        pk=pk
    )
    
    # Prepare additional context data
    context = {
        'artwork': artwork,
        # Use the model's helper method to get formatted size
        'size_display': artwork.get_size_display(),
        # Use the model's helper method to get formatted price
        'price_display': artwork.get_price_display(),
    }
    
    # Render the artwork detail template with the context data
    return render(request, 'Vistor_pages/artwork_detail.html', context)


def featured_artworks(request):
    """
    View to display featured artworks on the homepage or featured section.
    Shows a curated selection of artworks with price, size, and medium.
    
    Features:
    - Displays only featured artworks
    - Shows price, size, and medium for quick buyer information
    - Optimized for homepage display
    """
    from .models import Artwork
    
    # Fetch only featured artworks that are available
    # Using select_related to optimize database queries
    artworks = Artwork.objects.select_related('artist').filter(
        is_featured=True,
        is_available=True
    ).order_by('-created_at')
    
    # Limit to the most recent 6 featured artworks
    artworks = artworks[:6]
    
    # Prepare context data
    context = {
        'featured_artworks': artworks,
    }
    
    # Render the featured artworks template
    return render(request, 'Vistor_pages/featured_artworks.html', context)


def artworks_by_artist(request, artist_id):
    """
    View to display all artworks by a specific artist.
    Shows price, size, and medium for each artwork by the artist.
    
    Args:
        artist_id: ID of the artist whose artworks to display
    
    Features:
    - Displays all artworks by a specific artist
    - Shows price, size, and medium information
    - Includes artist profile information
    """
    from .models import Artwork
    from owner_app.models import ArtistProfile
    
    # Fetch the artist profile
    artist = get_object_or_404(ArtistProfile, pk=artist_id)
    
    # Fetch all artworks by this artist
    # Using filter to get artworks related to the artist
    artworks = Artwork.objects.filter(
        artist=artist,
        is_available=True
    ).order_by('-created_at')
    
    # Prepare context data
    context = {
        'artist': artist,
        'artworks': artworks,
    }
    
    # Render the artist artworks template
    return render(request, 'Vistor_pages/artworks_by_artist.html', context)


def artwork_search_by_price(request):
    """
    View to search and filter artworks by price range.
    Helps buyers find artworks within their budget.
    
    Features:
    - Filter artworks by minimum and maximum price
    - Display price, size, and medium for filtered results
    - Sort by price (ascending or descending)
    """
    from .models import Artwork
    
    # Get price range from query parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_order = request.GET.get('sort', 'asc')  # 'asc' or 'desc'
    
    # Start with all available artworks
    artworks = Artwork.objects.select_related('artist').filter(
        is_available=True
    )
    
    # Apply price filters if provided
    if min_price:
        artworks = artworks.filter(price__gte=min_price)
    if max_price:
        artworks = artworks.filter(price__lte=max_price)
    
    # Sort by price based on sort_order parameter
    if sort_order == 'desc':
        artworks = artworks.order_by('-price')
    else:
        artworks = artworks.order_by('price')
    
    # Prepare context data
    context = {
        'artworks': artworks,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
    }
    
    # Render the price search template
    return render(request, 'Vistor_pages/artwork_price_search.html', context)


# ============================================================================
# BASKET VIEWS - Shopping cart functionality
# ============================================================================

@login_required
def basket_view(request):
    """
    Display the user's shopping basket.
    Shows all items in the basket with quantities and prices.
    
    Features:
    - Displays all basket items
    - Shows individual item prices and subtotals
    - Calculates and displays total basket value
    - Provides links to update/remove items
    
    Requires:
    - User must be logged in
    """
    from .models import Basket
    
    # Get or create basket for the current user
    # This ensures every logged-in user has a basket
    basket, created = Basket.objects.get_or_create(user=request.user)
    
    # Get all items in the basket with related artwork data
    # Using select_related to optimize database queries
    basket_items = basket.items.select_related('artwork', 'artwork__artist').all()
    
    # Calculate basket totals
    total_price = basket.get_total_price()
    item_count = basket.get_item_count()
    
    # Prepare context data for template
    context = {
        'basket': basket,
        'basket_items': basket_items,
        'total_price': total_price,
        'item_count': item_count,
    }
    
    return render(request, 'Vistor_pages/basket.html', context)


@login_required
@require_POST
def add_to_basket(request, artwork_id):
    """
    Add an artwork to the user's basket.
    If the artwork is already in the basket, increase quantity.
    
    Args:
        artwork_id: ID of the artwork to add
    
    Features:
    - Creates basket if user doesn't have one
    - Adds artwork or updates quantity if already in basket
    - Stores current price as price_at_addition
    - Returns JSON response for AJAX requests
    - Redirects to basket or referrer for regular requests
    
    Requires:
    - User must be logged in
    - POST request only
    """
    from .models import Basket, BasketItem, Artwork
    
    # Get the artwork or return 404 if not found
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    # Check if artwork is available for purchase
    if not artwork.is_available:
        messages.error(request, f"Sorry, {artwork.title} is not available for purchase.")
        return redirect(request.META.get('HTTP_REFERER', 'collections_app:artwork_list'))
    
    # Check if artwork has a price
    if not artwork.price:
        messages.error(request, f"Sorry, {artwork.title} does not have a price set.")
        return redirect(request.META.get('HTTP_REFERER', 'collections_app:artwork_list'))
    
    # Get or create basket for the user
    basket, created = Basket.objects.get_or_create(user=request.user)
    
    # Get quantity from request (default to 1)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity
    if quantity < 1:
        quantity = 1
    
    # Check if artwork is already in basket
    basket_item, item_created = BasketItem.objects.get_or_create(
        basket=basket,
        artwork=artwork,
        defaults={
            'quantity': quantity,
            'price_at_addition': artwork.price
        }
    )
    
    # If item already existed, update quantity
    if not item_created:
        basket_item.quantity += quantity
        basket_item.save()
        messages.success(
            request,
            f"Updated {artwork.title} quantity to {basket_item.quantity} in your basket."
        )
    else:
        messages.success(
            request,
            f"Added {artwork.title} to your basket."
        )
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added {artwork.title} to basket",
            'basket_count': basket.get_item_count(),
            'basket_total': float(basket.get_total_price())
        })
    
    # Redirect to basket page or back to previous page
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'collections_app:basket'))
    return redirect(next_url)


@login_required
@require_POST
def update_basket_item(request, item_id):
    """
    Update the quantity of an item in the basket.
    
    Args:
        item_id: ID of the basket item to update
    
    Features:
    - Updates item quantity
    - Removes item if quantity is 0
    - Validates quantity is positive
    - Ensures item belongs to current user's basket
    
    Requires:
    - User must be logged in
    - POST request only
    """
    from .models import BasketItem
    
    # Get the basket item, ensuring it belongs to the current user
    basket_item = get_object_or_404(
        BasketItem,
        pk=item_id,
        basket__user=request.user
    )
    
    # Get new quantity from request
    new_quantity = int(request.POST.get('quantity', 1))
    
    # If quantity is 0 or less, remove the item
    if new_quantity <= 0:
        artwork_title = basket_item.artwork.title
        basket_item.delete()
        messages.success(request, f"Removed {artwork_title} from your basket.")
    else:
        # Update quantity
        basket_item.quantity = new_quantity
        basket_item.save()
        messages.success(
            request,
            f"Updated {basket_item.artwork.title} quantity to {new_quantity}."
        )
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        basket = basket_item.basket
        return JsonResponse({
            'success': True,
            'basket_count': basket.get_item_count(),
            'basket_total': float(basket.get_total_price()),
            'item_subtotal': float(basket_item.get_subtotal()) if new_quantity > 0 else 0
        })
    
    return redirect('collections_app:basket')


@login_required
@require_POST
def remove_from_basket(request, item_id):
    """
    Remove an item from the basket.
    
    Args:
        item_id: ID of the basket item to remove
    
    Features:
    - Removes item completely from basket
    - Ensures item belongs to current user's basket
    - Shows confirmation message
    
    Requires:
    - User must be logged in
    - POST request only
    """
    from .models import BasketItem
    
    # Get the basket item, ensuring it belongs to the current user
    basket_item = get_object_or_404(
        BasketItem,
        pk=item_id,
        basket__user=request.user
    )
    
    # Store artwork title before deletion
    artwork_title = basket_item.artwork.title
    basket = basket_item.basket
    
    # Delete the item
    basket_item.delete()
    
    messages.success(request, f"Removed {artwork_title} from your basket.")
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Removed {artwork_title} from basket",
            'basket_count': basket.get_item_count(),
            'basket_total': float(basket.get_total_price())
        })
    
    return redirect('collections_app:basket')


@login_required
@require_POST
def clear_basket(request):
    """
    Remove all items from the user's basket.
    
    Features:
    - Clears entire basket
    - Shows confirmation message
    - Useful for starting fresh or after order completion
    
    Requires:
    - User must be logged in
    - POST request only
    """
    from .models import Basket
    
    # Get user's basket
    try:
        basket = Basket.objects.get(user=request.user)
        # Clear all items
        basket.clear()
        messages.success(request, "Your basket has been cleared.")
    except Basket.DoesNotExist:
        messages.info(request, "Your basket is already empty.")
    
    return redirect('collections_app:basket')


def get_basket_count(request):
    """
    Get the number of items in the user's basket.
    Used for displaying basket count in navigation bar.
    
    Returns:
    - JSON response with basket count
    - Returns 0 if user is not logged in or has no basket
    
    Features:
    - Works for both logged-in and anonymous users
    - Lightweight query for navbar display
    - Returns JSON for AJAX requests
    """
    from .models import Basket
    
    # Return 0 if user is not authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    try:
        basket = Basket.objects.get(user=request.user)
        count = basket.get_item_count()
    except Basket.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})


# ============================================================================
# CHECKOUT VIEWS - Order processing and payment
# ============================================================================

@login_required
def checkout(request):
    """
    Display the checkout page with order summary and billing form.
    Users can review their basket items and enter billing information.
    
    Features:
    - Displays basket items with images, prices, and quantities
    - Shows order total and breakdown
    - Collects billing address information
    - Validates basket is not empty
    - Prepares order for payment processing
    
    Requires:
    - User must be logged in
    - Basket must contain at least one item
    
    Template:
    - Vistor_pages/checkout.html
    """
    from .models import Basket
    
    # Get user's basket
    try:
        basket = Basket.objects.prefetch_related(
            'items__artwork__artist'
        ).get(user=request.user)
        
        # Check if basket is empty
        if basket.get_item_count() == 0:
            messages.warning(request, "Your basket is empty. Please add items before checking out.")
            return redirect('collections_app:artwork_list')
        
        # Calculate totals
        subtotal = basket.get_total_price()
        # TODO: Add shipping cost calculation based on location
        shipping_cost = 0  # Free shipping for now
        total = subtotal + shipping_cost
        
    except Basket.DoesNotExist:
        messages.warning(request, "Your basket is empty. Please add items before checking out.")
        return redirect('collections_app:artwork_list')
    
    context = {
        'basket': basket,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'Vistor_pages/checkout.html', context)


# ============================================================================
# USER DASHBOARD VIEW
# ============================================================================
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):
    """
    Display the user dashboard with profile info and recent activity.
    """
    user = request.user
    # Example: fetch recent orders if implemented
    orders = []
    if hasattr(user, 'order_set'):
        orders = user.order_set.order_by('-created_at')[:5]
    return render(request, 'Vistor_pages/user_dashboard.html', {
        'user': user,
        'orders': orders,
    })

