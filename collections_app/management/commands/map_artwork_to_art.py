from django.core.management.base import BaseCommand
from collections_app.models import Artwork, Art, Collection, ArtVariant
from django.db import transaction


class Command(BaseCommand):
    help = 'Map existing Artwork records into Art. Dry-run by default; use --apply to write.'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Apply changes to DB')

    def handle(self, *args, **options):
        apply = options['apply']
        created = 0
        linked = 0
        unmatched = []

        artworks = Artwork.objects.select_related('artist').all()
        self.stdout.write(f'Found {artworks.count()} Artwork rows')

        if not apply:
            self.stdout.write('Dry-run mode: no DB writes will be made. Use --apply to write changes.')

        for artwork in artworks:
            # Try to find a candidate Art: same title, same artist via collection
            candidate = None
            # search for Art whose collection artist matches artwork.artist
            if artwork.artist:
                candidate = Art.objects.filter(title=artwork.title, collection__artist=artwork.artist).first()

            if candidate:
                linked += 1
                self.stdout.write(f'Linked Artwork {artwork.pk} -> Art {candidate.pk}')
                if apply:
                    # copy over fields if blank
                    if not candidate.price and artwork.price:
                        candidate.price = artwork.price
                    if not candidate.description and artwork.description:
                        candidate.description = artwork.description
                    if not candidate.is_available:
                        candidate.is_available = artwork.is_available
                    if not candidate.currency and artwork.currency:
                        candidate.currency = artwork.currency
                    # set artwork_link
                    candidate.artwork_link = artwork
                    candidate.save()
            else:
                unmatched.append(artwork.pk)
                self.stdout.write(f'Unmatched Artwork {artwork.pk} ({artwork.title})')
                if apply:
                    # create/imported collection per-artist
                    artist = artwork.artist
                    if artist:
                        coll, _ = Collection.objects.get_or_create(artist=artist, name='Imported')
                    else:
                        coll, _ = Collection.objects.get_or_create(artist=None, name='Imported')
                    art = Art.objects.create(
                        collection=coll,
                        title=artwork.title,
                        medium=artwork.medium,
                        year_created=artwork.year_created,
                        image=artwork.image,
                        width_cm=artwork.width_cm,
                        height_cm=artwork.height_cm,
                        # keep legacy fields for now but set ecommerce price
                        physical_available=artwork.is_available,
                        physical_price=artwork.price,
                        price=artwork.price,
                        currency=artwork.currency or 'USD',
                        description=artwork.description or '',
                        created_at=artwork.created_at,
                        updated_at=artwork.updated_at,
                        artwork_link=artwork,
                    )
                    created += 1
                    # Create ArtVariant(s) for this imported artwork
                    try:
                        if artwork.is_available and artwork.price:
                            ArtVariant.objects.create(
                                art=art,
                                medium=ArtVariant.ORIGINAL,
                                is_available=True,
                                price=artwork.price,
                                currency=artwork.currency or 'USD',
                            )
                        # Create placeholder poster/digital variants (not
                        # available by default)
                        ArtVariant.objects.get_or_create(
                            art=art,
                            medium=ArtVariant.POSTER,
                            defaults={'is_available': False},
                        )
                        ArtVariant.objects.get_or_create(
                            art=art,
                            medium=ArtVariant.DIGITAL,
                            defaults={'is_available': False},
                        )
                    except Exception:
                        # ignore variant creation errors in dry-run
                        # environments
                        pass

        self.stdout.write('--- Summary ---')
        self.stdout.write(f'Linked: {linked}')
        self.stdout.write(f'Created: {created}')
        self.stdout.write(f'Unmatched count: {len(unmatched)}')

        # Backfill basket/order art FKs when applying
        if apply:
            from collections_app.models import BasketItem, OrderItem

            bi_updated = 0
            oi_updated = 0

            # Backfill BasketItem.art where possible
            for bi in BasketItem.objects.filter(
                art__isnull=True, artwork__isnull=False
            ):
                linked_art = getattr(bi.artwork, 'linked_art', None)
                if linked_art:
                    bi.art = linked_art
                    bi.save(update_fields=['art'])
                    bi_updated += 1

            # Backfill OrderItem.art where possible
            for oi in OrderItem.objects.filter(
                art__isnull=True, artwork__isnull=False
            ):
                linked_art = getattr(oi.artwork, 'linked_art', None)
                if linked_art:
                    oi.art = linked_art
                    oi.save(update_fields=['art'])
                    oi_updated += 1

            self.stdout.write(f'BasketItems updated: {bi_updated}')
            self.stdout.write(f'OrderItems updated: {oi_updated}')
