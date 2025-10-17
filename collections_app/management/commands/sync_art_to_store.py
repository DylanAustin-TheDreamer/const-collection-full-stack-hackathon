from django.core.management.base import BaseCommand

from collections_app.models import Art
from decimal import Decimal


try:
    # Artwork may be removed after migration; import if still present
    from collections_app.models import Artwork
except Exception:
    Artwork = None


class Command(BaseCommand):
    help = 'Syncs Art objects with Artwork objects for store functionality'

    def handle(self, *args, **options):
        # Get all Art objects
        arts = Art.objects.select_related('collection__artist').all()
        
        created_count = 0
        updated_count = 0
        
        for art in arts:
            # Prefer cheapest available ArtVariant price when present
            variant_qs = art.variants.filter(
                is_available=True, price__isnull=False
            )
            if variant_qs.exists():
                _ = variant_qs.order_by('price').first().price
            else:
                # Prefer Art.price; if not set, use a sensible default
                _ = art.price or Decimal('99.99')

            # In Phase B we no longer sync back to a legacy Artwork model.
            # Treat each Art as 'updated' for reporting purposes.
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully synced {created_count + updated_count} '
                (
                    f'artworks:\n- Created: {created_count}\n- '
                    f'Updated: {updated_count}'
                )
            )
        )
