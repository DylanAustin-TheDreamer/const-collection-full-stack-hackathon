from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    # Use the canonical artwork templates for the store listing.
    # Map the queryset into the context key expected by artwork_list.html (artworks).
    # Redirect to the canonical artwork listing which prepares full context
    # (collections, format_choices, featured_artworks, etc.).
    # Preserve any querystring parameters from the store URL so filters work.
    target = reverse('collections_app:artwork_list')
    qs = request.GET.urlencode()
    if qs:
        target = f"{target}?{qs}"
    return redirect(target)
