from django.shortcuts import render

def index(request):
    from collections_app.models import Artwork

    sale_items = (
        Artwork.objects
        .filter(is_available=True)
        .select_related('artist')
        .order_by('-created_at')
    )

    return render(
        request,
        'Vistor_pages/store.html',
        {'sale_items': sale_items},
    )
