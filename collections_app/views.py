from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, Http404
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order, OrderItem
import os
import mimetypes


def index(request):
    # Serve the homepage at root by rendering Vistor_pages/home.html
    from .models import Media
    
    context = {}
    try:
        # Get the hero media (should be a video)
        hero_media = Media.objects.filter(hero=True).first()
        
        # Get the secondary media (second_section video)
        secondary_media = Media.objects.filter(second_section=True).first()
        
        if hero_media and hero_media.file:
            context['hero_video'] = hero_media.file.url
        else:
            context['hero_video'] = None  # Or a fallback static video
            
        if secondary_media and secondary_media.file:
            context['secondary_video'] = secondary_media.file.url
        else:
            context['secondary_video'] = None  # Or a fallback static video
            
    except Exception as e:
        # Handle any database errors gracefully
        context['hero_video'] = None
        context['secondary_video'] = None
        print(f"Media error: {e}")  # For debugging
    
    return render(request, 'Vistor_pages/home.html', context)


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

    # For compatibility keep 'artwork' context key pointing to the Art instance
    return render(request, 'Vistor_pages/art_detail.html', {
        'art': art,
        'artwork': art,
    })


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
    from .models import Art, Collection, ArtVariant

    # Fetch all art rows (Art is canonical) and expose them as 'artworks' for templates
    # Prefetch variants so templates can show per-medium pricing without N+1
    artworks = (
        Art.objects
        .select_related('collection__artist')
        .prefetch_related('variants')
        .all()
    )

    # Only show arts that have at least one available variant
    artworks = artworks.filter(variants__is_available=True).distinct()
    
    # Get search query from URL parameters (if provided)
    search_query = request.GET.get('search', '')
    if search_query:
        # Filter artworks by title, medium, or artist name
        artworks = artworks.filter(
            Q(title__icontains=search_query) |
            Q(medium__icontains=search_query) |
            Q(collection__artist__name__icontains=search_query)
        )
    
    # Filter by collection (if provided)
    selected_collection = request.GET.get('collection', '')
    if selected_collection:
        artworks = artworks.filter(collection__id=selected_collection)

    # Filter by available format (ArtVariant.medium)
    selected_format = request.GET.get('format', '')
    if selected_format:
        artworks = artworks.filter(variants__medium=selected_format, variants__is_available=True)
    
    # Order artworks by creation date (newest first)
    artworks = artworks.order_by('-created_at')
    
    # Prepare context data to pass to the template
    # Provide collections and format choices for the filter UI and featured artworks
    collections = Collection.objects.select_related('artist').all()
    format_choices = ArtVariant.MEDIUM_CHOICES
    # Include featured artworks even when `Art.is_available` is False but the
    # artwork has at least one available ArtVariant. Availability is often
    # derived from variants, so this ensures featured pieces surface correctly.
    featured_artworks = (
        Art.objects
        .filter(is_featured=True)
        .filter(Q(is_available=True) | Q(variants__is_available=True))
        .distinct()
        .order_by('-created_at')[:6]
    )

    context = {
        'artworks': artworks,
        'search_query': search_query,
        'collections': collections,
        'format_choices': format_choices,
        'selected_collection': selected_collection,
        'selected_format': selected_format,
        'featured_artworks': featured_artworks,
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
    from .models import Art

    # Fetch the Art row and present it under 'artwork' for templates
    art = get_object_or_404(
        Art.objects.select_related('collection__artist').prefetch_related('variants'),
        pk=pk
    )

    # Prepare variant information for the template
    variants_qs = list(art.variants.all())

    # Build a mapping for medium -> variant and order by desired priority
    variants_map = {v.medium: v for v in variants_qs}
    preferred_order = [
        'original_piece',
        'printed_poster',
        'digital_copy',
    ]
    variants = [variants_map[k] for k in preferred_order if k in variants_map]

    # Determine main price display: prefer ORIGINAL then POSTER then DIGITAL when available
    price_display = None
    default_variant_pk = None
    for medium_key in preferred_order:
        v = variants_map.get(medium_key)
        if v and v.is_available and v.price is not None:
            price_display = f"{v.currency} {v.price:,.2f}"
            default_variant_pk = v.pk
            break
    # Fallback: use any available variant with a price
    if price_display is None:
        for v in variants_qs:
            if v.is_available and v.price is not None:
                price_display = f"{v.currency} {v.price:,.2f}"
                default_variant_pk = v.pk
                break
    # Final fallback: art-level price display
    if price_display is None:
        price_display = art.get_price_display()

    context = {
        'artwork': art,
        'size_display': art.get_size_display(),
        'price_display': price_display,
        'variants': variants,
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
    from .models import Art

    artworks = (
        Art.objects.select_related('collection__artist')
        .filter(is_featured=True, is_available=True)
        .order_by('-created_at')
    )
    
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
    from .models import Art
    from owner_app.models import ArtistProfile
    
    # Fetch the artist profile
    artist = get_object_or_404(ArtistProfile, pk=artist_id)
    
    # Fetch all artworks by this artist
    # Using filter to get artworks related to the artist
    # Art does not have direct artist FK; filter via collection__artist
    artworks = Art.objects.select_related('collection__artist').filter(
        collection__artist=artist,
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
    from .models import Art

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_order = request.GET.get('sort', 'asc')

    artworks = (
        Art.objects.select_related('collection__artist')
        .filter(is_available=True)
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
    
    # Get all items in the basket with related artwork/art data
    # Prefer 'art' (canonical) but keep Artwork for compatibility
    basket_items = (
        basket.items
        .select_related(
            'art',
            'art__collection__artist',
        )
        .all()
    )
    
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
    from .models import Basket, BasketItem, Art

    # We now use the canonical Art model; Artwork DB rows have been removed.
    artwork = get_object_or_404(Art, pk=artwork_id)

    # Phase B: variant selection is required
    variant_id = request.POST.get('variant_id')
    if not variant_id:
        messages.error(
            request,
            'Please select a format/variant before adding to basket.',
        )
        return redirect(
            request.META.get('HTTP_REFERER', 'collections_app:artwork_list')
        )

    from .models import ArtVariant
    try:
        variant = ArtVariant.objects.get(pk=int(variant_id), art=artwork)
    except ArtVariant.DoesNotExist:
        messages.error(request, 'Selected format is invalid.')
        return redirect(
            request.META.get('HTTP_REFERER', 'collections_app:artwork_list')
        )

    # Validate availability/price using variant if provided,
    # otherwise fall back to art
    if variant:
        if not variant.is_available:
            msg = (
                f"Sorry, {artwork.title} "
                f"({variant.get_medium_display()}) is unavailable."
            )
            messages.error(request, msg)
            return redirect(
                request.META.get(
                    'HTTP_REFERER', 'collections_app:artwork_list'
                )
            )
        if variant.price is None:
            msg = (
                f"Sorry, {artwork.title} "
                f"({variant.get_medium_display()}) has no price set."
            )
            messages.error(request, msg)
            return redirect(
                request.META.get(
                    'HTTP_REFERER', 'collections_app:artwork_list'
                )
            )
    else:
        if not getattr(artwork, 'is_available', True):
            messages.error(
                request,
                f"Sorry, {artwork.title} is not available for purchase."
            )
            return redirect(
                request.META.get(
                    'HTTP_REFERER', 'collections_app:artwork_list'
                )
            )
        if not getattr(artwork, 'price', None):
            messages.error(
                request,
                f"Sorry, {artwork.title} does not have a price set."
            )
            return redirect(
                request.META.get(
                    'HTTP_REFERER', 'collections_app:artwork_list'
                )
            )
    
    # Get or create basket for the user
    basket, created = Basket.objects.get_or_create(user=request.user)
    
    # Get quantity from request (default to 1)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity
    if quantity < 1:
        quantity = 1
    
    # Create or update BasketItem linked to the canonical Art model
    # (and optional variant)
    defaults = {'quantity': quantity}
    if variant:
        defaults['price_at_addition'] = variant.price
    else:
        defaults['price_at_addition'] = artwork.price

    basket_item, item_created = BasketItem.objects.get_or_create(
        basket=basket,
        art=artwork,
        variant=variant,
        defaults=defaults,
    )
    
    # If item already existed, update quantity
    if not item_created:
        basket_item.quantity += quantity
        basket_item.save()
        messages.success(
            request,
            (
                f"Updated {artwork.title} quantity to "
                f"{basket_item.quantity} in your basket."
            )
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
    next_url = request.POST.get(
        'next', request.META.get('HTTP_REFERER', 'collections_app:basket')
    )
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
        display = getattr(basket_item, 'display_artwork', None)
        artwork_title = display.title if display else 'Unknown artwork'
        basket_item.delete()
        messages.success(request, f"Removed {artwork_title} from your basket.")
    else:
        # Update quantity
        basket_item.quantity = new_quantity
        basket_item.save()
        display = getattr(basket_item, 'display_artwork', None)
        title = display.title if display else 'Unknown artwork'
        messages.success(
            request,
            f"Updated {title} quantity to {new_quantity}."
        )
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        basket = basket_item.basket
        return JsonResponse({
            'success': True,
            'basket_count': basket.get_item_count(),
            'basket_total': float(basket.get_total_price()),
            'item_subtotal': (
                float(basket_item.get_subtotal()) if new_quantity > 0 else 0
            )
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
    display = getattr(basket_item, 'display_artwork', None)
    artwork_title = display.title if display else 'Unknown artwork'
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
        # Prefetch related art and artist via the art->collection->artist path
        basket = Basket.objects.prefetch_related(
            'items__art__collection__artist'
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

        # If this is a POST from the checkout form, create an Order (admin test checkout)
        if request.method == 'POST':
            # Create order using submitted billing fields
            order = None
            try:
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    payment_method='admin-test',
                    stripe_payment_intent='TEST',
                    email=request.POST.get('email', request.user.email or ''),
                    full_name=f"{request.POST.get('first_name','') } {request.POST.get('last_name','')}",
                    address_line1=request.POST.get('address_line1',''),
                    address_line2=request.POST.get('address_line2',''),
                    city=request.POST.get('city',''),
                    postal_code=request.POST.get('postal_code',''),
                    country=request.POST.get('country','') or 'US',
                )

                # Create OrderItems from BasketItems
                for bi in basket.items.all():
                    display = getattr(bi, 'display_artwork', None)
                    variant_obj = getattr(bi, 'variant', None)
                    OrderItem.objects.create(
                        order=order,
                        art=(bi.art if getattr(bi, 'art', None) else None),
                        artwork_title=(
                            display.title if display else bi.price_at_addition
                        ),
                        artwork_artist=(
                            display.artist.name
                            if getattr(display, 'artist', None)
                            else ''
                        ),
                        artwork_medium=(
                            display.medium
                            if getattr(display, 'medium', None)
                            else ''
                        ),
                        quantity=bi.quantity,
                        price=bi.price_at_addition,
                        # snapshot selected variant info when available
                        variant_id=(variant_obj.pk if variant_obj else None),
                        variant_medium=(
                            variant_obj.get_medium_display()
                            if variant_obj
                            else ''
                        ),
                    )

                # Clear the basket
                basket.clear()

                messages.success(
                    request,
                    f'Payment successful! Order #{order.order_number}',
                )
                return redirect(
                    'collections_app:order_success', order_id=order.id
                )

            except Exception as exc:
                messages.error(request, f"Failed to create order: {exc}")
                # Fall through to render the checkout page with an error

    except Basket.DoesNotExist:
        messages.warning(
            request,
            "Your basket is empty. Please add items before checking out.",
        )
        return redirect('collections_app:artwork_list')
    
    context = {
        'basket': basket,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'Vistor_pages/checkout.html', context)


@login_required
def order_success(request, order_id):
    """Minimal order success page for admin test checkouts."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'Vistor_pages/order_success.html', {'order': order})


# ============================================================================
# USER DASHBOARD VIEW
# ============================================================================

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


def manage_media(request):
    """Simple view for superusers to add/manage Media entries outside admin.

    This is intentionally lightweight: it displays a form for creating Media and
    lists recent media items. The canonical admin is still recommended.
    """
    if not getattr(request.user, 'is_superuser', False):
        return HttpResponseForbidden('Only superusers can access this page')

    from .forms import MediaForm
    from .models import Media

    try:
        if request.method == 'POST':
            form = MediaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('collections_app:manage_media')
        else:
            form = MediaForm()

        # Build a simple recent list using the current Media columns only.
        recent_rows = list(
            Media.objects.order_by('-created_at').values(
                'id',
                'file',
                'media_type',
                'caption',
                'hero',
                'second_section',
                'third_section',
                'created_at',
            )[:50]
        )

        recent = []
        for row in recent_rows:
            recent.append(
                {
                    'id': row.get('id'),
                    'has_file': bool(row.get('file')),
                    'media_type': row.get('media_type'),
                    'caption': row.get('caption'),
                    'hero': bool(row.get('hero')),
                    'second_section': bool(row.get('second_section')),
                    'third_section': bool(row.get('third_section')),
                    'created_at': row.get('created_at'),
                }
            )

        return render(
            request,
            'owner_pages/media_manage.html',
            {'form': form, 'recent': recent},
        )
    except Exception as exc:
        # Catch-all so owners see a friendly page instead of a 500 while we
        # investigate root causes (e.g. orphaned rows).
        messages.error(request, f'Error loading media manager: {exc}')
        form = MediaForm()
        return render(
            request,
            'owner_pages/media_manage.html',
            {'form': form, 'recent': []},
        )


def edit_media(request, pk):
    """Edit an existing Media row (superuser-only)."""
    if not getattr(request.user, 'is_superuser', False):
        return HttpResponseForbidden('Only superusers can edit media')

    from .models import Media
    from .forms import MediaForm

    media = get_object_or_404(Media, pk=pk)
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated')
            return redirect('collections_app:manage_media')
    else:
        form = MediaForm(instance=media)

    return render(request, 'owner_pages/media_edit.html', {'form': form, 'media': media})


@login_required
def delete_media(request, pk):
    # restrict to superusers
    if not getattr(request.user, 'is_superuser', False):
        return HttpResponseForbidden('Only superusers can delete media')

    from .models import Media
    media = get_object_or_404(Media, pk=pk)
    if request.method == 'POST':
        media.delete()
        return redirect('collections_app:manage_media')
    return render(
        request,
        'owner_pages/confirm_delete.html',
        {'object': media, 'type': 'Media'},
    )
def contact(request):
    """Contact page that displays contact information from the database."""
    from owner_app.models import Contact
    
    contact_info = Contact.objects.first()
    
    context = {}
    if contact_info:
        context = {
            'address_line_1': contact_info.address_line_1,
            'address_line_2': contact_info.address_line_2,
            'city': contact_info.city,
            'zip_code': contact_info.zip_code,
            'phone': contact_info.phone,
            'email': contact_info.email,
            'curator_name': contact_info.curator_name,
            'curator_email': contact_info.curator_email,
            'opening_hours': contact_info.opening_hours,
        }
    
    return render(request, 'Vistor_pages/contact.html', context)


def web_build(request):
    """Serve the Unity WebGL build"""
    response = render(request, 'web_build/index.html')
    # Add Unity-specific headers
    response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response


def serve_unity_file(request, file_path):
    """Serve Unity WebGL files with proper MIME types and headers"""
    # Build the full file path
    build_dir = os.path.join(settings.BASE_DIR, 'templates', 'web_build')
    full_path = os.path.join(build_dir, file_path)
    
    if not os.path.exists(full_path):
        raise Http404("Unity file not found")
    
    # Determine content type based on file extension
    content_type = 'application/octet-stream'
    encoding = None
    
    if file_path.endswith('.wasm.gz'):
        content_type = 'application/wasm'
        encoding = 'gzip'
    elif file_path.endswith('.data.gz'):
        content_type = 'application/octet-stream'
        encoding = 'gzip'
    elif file_path.endswith('.js.gz'):
        content_type = 'application/javascript'
        encoding = 'gzip'
    elif file_path.endswith('.js'):
        content_type = 'application/javascript'
    elif file_path.endswith('.wasm'):
        content_type = 'application/wasm'
    
    # Read and serve the file
    with open(full_path, 'rb') as f:
        content = f.read()
    
    response = HttpResponse(content, content_type=content_type)
    
    # Add encoding header for gzipped files
    if encoding:
        response['Content-Encoding'] = encoding
    
    # Add Unity-specific headers
    response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response['Cross-Origin-Opener-Policy'] = 'same-origin'
    
    return response

