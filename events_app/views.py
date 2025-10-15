from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import Exhibition


def index(request):
    """Show events page with upcoming and previous exhibitions.

    Upcoming: no end_date (ongoing) or end_date >= today.
    Previous: end_date < today.
    """
    today = timezone.localdate()

    upcoming_exhibitions = (
        Exhibition.objects
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=today))
        .order_by('start_date')
    )

    previous_exhibitions = (
        Exhibition.objects.filter(end_date__lt=today)
        .order_by('-end_date')
    )

    context = {
        'upcoming_exhibitions': upcoming_exhibitions,
        'previous_exhibitions': previous_exhibitions,
    }

    return render(request, 'Vistor_pages/events.html', context)


def detail(request, pk):
    """Exhibition detail page showing exhibition info and included artworks."""
    exhibition = get_object_or_404(Exhibition, pk=pk)

    # Select related art and collection for efficient rendering
    exhibition_arts = exhibition.exhibition_arts.select_related(
        'art__collection'
    ).all()

    return render(
        request,
        'Vistor_pages/exhibition_detail.html',
        {
            'exhibition': exhibition,
            'exhibition_arts': exhibition_arts,
        },
    )
