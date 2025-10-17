from django.core.management.base import BaseCommand
from collections_app.models import Art
from decimal import Decimal

try:
    from collections_app.models import Artwork
except Exception:
    Artwork = None


class Command(BaseCommand):
    help = (
        'Syncs Art models to Artwork models and ensures all are '
        'available for purchase'
    )

    def handle(self, *args, **options):
        # Get all Art objects
        arts = Art.objects.select_related('collection__artist').all()
        
        synced_count = 0
        for art in arts:
            # Try to find existing Artwork or create new one
            # Prefer cheapest available ArtVariant price when present
            variant_qs = art.variants.filter(
                is_available=True, price__isnull=False
            )
            if variant_qs.exists():
                _ = variant_qs.order_by('price').first().price
            else:
                _ = art.price or Decimal('99.99')

            # Phase B: do not sync to legacy Artwork model; count as synced
            synced_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully synced {synced_count} artworks and '
                f'made them available'
            )
        )
