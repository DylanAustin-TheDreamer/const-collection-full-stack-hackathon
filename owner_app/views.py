from django.shortcuts import render, redirect
from .models import ArtistProfile, Contact
from .forms import ArtistProfileForm, ContactForm
from collections_app.forms import ArtForm
from collections_app.forms_collection import CollectionForm
from collections_app.models import Art, Media
from collections_app.models import Collection
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
    contact = Contact.objects.first()
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'artist_submit' in request.POST:
            # Artist form was submitted
            artist_form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
            if artist_form.is_valid():
                artist_form.save()
                return redirect('owner_app:edit_artist')
            # If artist form is invalid, create contact form for display
            contact_form = ContactForm(instance=contact)
        elif 'contact_submit' in request.POST:
            # Contact form was submitted
            contact_form = ContactForm(request.POST, instance=contact)
            if contact_form.is_valid():
                contact_form.save()
                return redirect('owner_app:edit_artist')
            # If contact form is invalid, create artist form for display
            artist_form = ArtistProfileForm(instance=artist)
    else:
        # GET request - show both forms
        artist_form = ArtistProfileForm(instance=artist)
        contact_form = ContactForm(instance=contact)

    return render(
        request,
        'owner_pages/edit_about.html',
        {
            'artist_form': artist_form, 
            'contact_form': contact_form,
            'artist': artist,
            'contact': contact,
        },
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
def delete_art(request, pk):
    art = Art.objects.get(pk=pk)
    if request.method == 'POST':
        art.delete()
        return redirect('owner_app:art_list')
    return render(
        request,
        'owner_pages/confirm_delete.html',
        {'object': art, 'type': 'Art'},
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
def collections_list(request):
    """Owner view: list collections with edit links."""
    collections = Collection.objects.select_related('artist').all()
    return render(
        request,
        'owner_pages/collections_list.html',
        {'collections': collections},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner_app:collections_list')
    else:
        form = CollectionForm()

    return render(
        request,
        'owner_pages/collection_form.html',
        {'form': form},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def edit_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('owner_app:collections_list')
    else:
        form = CollectionForm(instance=collection)

    return render(
        request,
        'owner_pages/collection_form.html',
        {'form': form, 'collection': collection, 'edit': True},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.method == 'POST':
        collection.delete()
        return redirect('owner_app:collections_list')
    return render(
        request,
        'owner_pages/confirm_delete.html',
        {'object': collection, 'type': 'Collection'},
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
def edit_exhibition(request, pk):
    exhibition = Exhibition.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, request.FILES, instance=exhibition)
        if form.is_valid():
            form.save()
            return redirect('owner_app:exhibitions_list')
    else:
        form = ExhibitionForm(instance=exhibition)

    return render(
        request,
        'owner_pages/exhibition_form.html',
        {'form': form, 'exhibition': exhibition},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def delete_exhibition(request, pk):
    exhibition = Exhibition.objects.get(pk=pk)
    if request.method == 'POST':
        exhibition.delete()
        return redirect('owner_app:exhibitions_list')
    return render(
        request,
        'owner_pages/confirm_delete.html',
        {'object': exhibition, 'type': 'Exhibition'},
    )


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


@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def assign_media(request, exhibition_pk):
    """Allow owner to select Media rows to include in an exhibition."""
    from events_app.models import ExhibitionMedia

    exhibition = Exhibition.objects.get(pk=exhibition_pk)

    all_media = Media.objects.order_by('-created_at').all()

    existing_ids = set(
        exhibition.exhibition_media.values_list('media_id', flat=True)
    )

    if request.method == 'POST':
        selected = request.POST.getlist('media')
        selected_ids = set(int(i) for i in selected)

        # add newly selected
        for media_id in selected_ids - existing_ids:
            ExhibitionMedia.objects.get_or_create(
                exhibition=exhibition, media_id=media_id
            )

        # remove unselected
        for media_id in existing_ids - selected_ids:
            ExhibitionMedia.objects.filter(
                exhibition=exhibition, media_id=media_id
            ).delete()

        return redirect('owner_app:exhibitions_list')

    return render(
        request,
        'owner_pages/assign_media.html',
        {
            'exhibition': exhibition,
            'all_media': all_media,
            'existing_ids': existing_ids,
        },
    )


