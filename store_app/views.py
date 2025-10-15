from django.shortcuts import render
from django.db import models


def index(request):
    from collections_app.models import Art

    sale_items = (
        Art.objects.filter(
            models.Q(physical_available=True)
            | models.Q(digital_available=True)
        )
        .select_related('collection', 'collection__artist')
    )

    return render(
        request,
        'Vistor_pages/store.html',
        {'sale_items': sale_items},
    )
