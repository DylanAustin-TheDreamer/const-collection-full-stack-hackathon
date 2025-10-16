from django.shortcuts import render, get_object_or_404
from django.db.models import Q


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
