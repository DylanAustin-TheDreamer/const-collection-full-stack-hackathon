from django.shortcuts import render, redirect
from .models import ArtistProfile, Contact
from .forms import ArtistProfileForm, ContactForm
from collections_app.forms import ArtForm
from collections_app.forms_collection import CollectionForm
from collections_app.models import Art, Media, ArtVariant, BasketItem
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def edit_artist(request):
    artist = ArtistProfile.objects.first()
    contact = Contact.objects.first()
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'artist_submit' in request.POST:
            # Artist form was submitted
            artist_form = ArtistProfileForm(
                request.POST,
                request.FILES,
                instance=artist,
            )
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def art_list(request):
    # Group arts by collection for owner listing
    collections = (
        Collection.objects.prefetch_related('arts')
        .select_related('artist')
        .all()
    )
    # Prepare a mapping of collection -> arts queryset
    grouped = []
    for coll in collections:
        grouped.append({'collection': coll, 'arts': coll.arts.all()})
    return render(
        request,
        'owner_pages/art_list.html',
        {'grouped_collections': grouped},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def toggle_featured_art(request, pk):
    """Toggle the is_featured flag for an Art (owner action).

    This is a simple POST endpoint that flips the boolean and redirects
    back to the owner art list.
    """
    art = Art.objects.get(pk=pk)
    if request.method == 'POST':
        art.is_featured = not art.is_featured
        art.save()
    return redirect('owner_app:art_list')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def delete_art(request, pk):
    art = Art.objects.get(pk=pk)
    # Dependent counts: variants and any basket items referencing those variants
    variant_qs = art.variants.all()
    variant_count = variant_qs.count()
    basket_qs = BasketItem.objects.filter(variant__art=art)
    basket_count = basket_qs.count()

    variant_names = list(variant_qs.values_list('medium', flat=True)[:10])

    if request.method == 'POST':
        # Remove basket items that would PROTECT deletion of variants
        if basket_count:
            basket_qs.delete()
        art.delete()
        return redirect('owner_app:art_list')

    return render(
        request,
        'owner_pages/confirm_delete.html',
        {
            'object': art,
            'type': 'Art',
            'dependent': {
                'variant_count': variant_count,
                'basket_count': basket_count,
                'variant_names': variant_names,
            },
        },
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def exhibitions_list(request):
    exhibitions = Exhibition.objects.order_by('-start_date')
    return render(
        request,
        'owner_pages/exhibitions_list.html',
        {'exhibitions': exhibitions},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def collections_list(request):
    """Owner view: list collections with edit links."""
    collections = Collection.objects.select_related('artist').all()
    return render(
        request,
        'owner_pages/collections_list.html',
        {'collections': collections},
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def delete_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    # Gather dependent objects so we can show a clear confirmation page
    arts_qs = Art.objects.filter(collection=collection)
    art_count = arts_qs.count()
    variant_qs = ArtVariant.objects.filter(art__collection=collection)
    variant_count = variant_qs.count()
    # Basket items reference ArtVariant via required FK with PROTECT; these
    # must be removed before we can delete the variants/art/collection.
    basket_qs = BasketItem.objects.filter(variant__art__collection=collection)
    basket_count = basket_qs.count()

    # Provide a short preview list of art titles for the confirmation page
    art_titles = list(arts_qs.values_list('title', flat=True)[:20])

    if request.method == 'POST':
        # First remove dependent BasketItems which would otherwise PROTECT
        # deletion of ArtVariant (and therefore prevent collection deletion).
        if basket_count:
            basket_qs.delete()

        # Deleting the collection will cascade-delete its Art and ArtVariant
        # rows (Art.collection and ArtVariant.art are CASCADE).
        collection.delete()
        return redirect('owner_app:collections_list')

    return render(
        request,
        'owner_pages/confirm_delete.html',
        {
            'object': collection,
            'type': 'Collection',
            'dependent': {
                'art_count': art_count,
                'variant_count': variant_count,
                'basket_count': basket_count,
                'art_titles': art_titles,
            },
        },
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def create_exhibition(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner_app:exhibitions_list')
    else:
        form = ExhibitionForm()

    return render(request, 'owner_pages/exhibition_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def delete_exhibition(request, pk):
    exhibition = Exhibition.objects.get(pk=pk)
    # Count linked items (ExhibitionArt, ExhibitionMedia)
    art_links = exhibition.exhibition_arts.count()
    media_links = exhibition.exhibition_media.count()
    art_titles = list(exhibition.exhibition_arts.select_related('art').values_list('art__title', flat=True)[:20])

    if request.method == 'POST':
        # Do NOT delete linked ExhibitionArt / ExhibitionMedia rows.
        # Those links do not require the Exhibition to be removed and should
        # remain intact for archival or reporting purposes. Only delete the
        # Exhibition DB row here; avoid attempting to remove remote assets
        # (cover image) from storage — leaving orphaned media is preferable
        # to failing the whole delete request.
        exhibition.delete()
        return redirect('owner_app:exhibitions_list')

    return render(
        request,
        'owner_pages/confirm_delete.html',
        {
            'object': exhibition,
            'type': 'Exhibition',
            'dependent': {
                'art_count': art_links,
                'media_count': media_links,
                'art_titles': art_titles,
            },
        },
    )


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
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


