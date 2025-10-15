from django.shortcuts import render, redirect
from .models import ArtistProfile
from .forms import ArtistProfileForm
from collections_app.forms import ArtForm
from collections_app.forms_collection import CollectionForm
from collections_app.models import Art
from events_app.forms import ExhibitionForm
from events_app.models import Exhibition
from django.contrib.auth.decorators import user_passes_test


def index(request):
    artist = ArtistProfile.objects.first()
    return render(request, 'owner_pages/about.html', {'artist': artist})


def public_about(request):
    """Public about page used by visitors."""
    artist = ArtistProfile.objects.first()
    return render(request, 'Vistor_pages/about.html', {'artist': artist})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def edit_artist(request):
    artist = ArtistProfile.objects.first()
    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('about')
    else:
        form = ArtistProfileForm(instance=artist)

    return render(
        request,
        'owner_pages/edit_about.html',
        {'form': form, 'artist': artist},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def art_list(request):
    arts = Art.objects.select_related('collection', 'collection__artist').all()
    return render(request, 'owner_pages/art_list.html', {'arts': arts})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def create_art(request):
    # Support inline collection creation from the same page.
    collection_form = CollectionForm()

    if request.method == 'POST':
        # If the post has 'create_collection' we process collection form first
        if 'create_collection' in request.POST:
            collection_form = CollectionForm(request.POST, request.FILES)
            if collection_form.is_valid():
                collection = collection_form.save()
                # After creating collection, render art form with new
                # collection selected
                form = ArtForm(initial={'collection': collection.pk})
                return render(
                    request,
                    'owner_pages/art_form.html',
                    {
                        'form': form,
                        'collection_form': collection_form,
                        'created_collection': collection,
                    },
                )

        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner_app:art_list')
    else:
        form = ArtForm()

    return render(
        request,
        'owner_pages/art_form.html',
        {'form': form, 'collection_form': collection_form},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def edit_art(request, pk):
    art = Art.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArtForm(request.POST, request.FILES, instance=art)
        if form.is_valid():
            form.save()
            return redirect('owner_app:art_list')
    else:
        form = ArtForm(instance=art)

    return render(
        request,
        'owner_pages/art_form.html',
        {'form': form, 'edit': True, 'art': art},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def exhibitions_list(request):
    exhibitions = Exhibition.objects.order_by('-start_date')
    return render(
        request,
        'owner_pages/exhibitions_list.html',
        {'exhibitions': exhibitions},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def create_exhibition(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner_app:exhibitions_list')
    else:
        form = ExhibitionForm()

    return render(request, 'owner_pages/exhibition_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def assign_art(request, exhibition_pk):
    """Allow owner to select artworks to include in an exhibition.

    The form will display all Art (title + thumbnail) with checkboxes.
    On POST, the selection will be used to create/delete ExhibitionArt links
    so the selection is authoritative.
    """
    from events_app.models import ExhibitionArt

    exhibition = Exhibition.objects.get(pk=exhibition_pk)

    all_art = Art.objects.select_related('collection').all()

    # existing art ids linked to this exhibition
    existing_ids = set(
        exhibition.exhibition_arts.values_list('art_id', flat=True)
    )

    if request.method == 'POST':
        selected = request.POST.getlist('art')
        selected_ids = set(int(i) for i in selected)

        # create links for newly selected
        for art_id in selected_ids - existing_ids:
            ExhibitionArt.objects.get_or_create(
                exhibition=exhibition, art_id=art_id
            )

        # remove links for unselected
        for art_id in existing_ids - selected_ids:
            ExhibitionArt.objects.filter(
                exhibition=exhibition, art_id=art_id
            ).delete()

        return redirect('owner_app:exhibitions_list')

    return render(
        request,
        'owner_pages/assign_art.html',
        {
            'exhibition': exhibition,
            'all_art': all_art,
            'existing_ids': existing_ids,
        },
    )
