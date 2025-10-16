from django.shortcuts import render


def index(request):
    # Use the canonical artwork templates for the store listing.
    # Map the queryset into the context key expected by artwork_list.html (artworks).
    from collections_app.models import Art

    sale_items = (
        Art.objects
        .filter(is_available=True)
        .select_related('collection__artist')
        .order_by('-created_at')
    )

    return render(
        request,
        'Vistor_pages/artwork_list.html',
        {'artworks': sale_items},
    )
