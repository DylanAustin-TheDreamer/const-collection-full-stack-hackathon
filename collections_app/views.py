from django.shortcuts import render


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
