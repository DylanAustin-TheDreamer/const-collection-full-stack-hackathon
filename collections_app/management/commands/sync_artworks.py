from django.core.management.base import BaseCommand
from collections_app.models import Art, Artwork

class Command(BaseCommand):
    help = 'Syncs Art models to Artwork models and ensures all are available for purchase'

    def handle(self, *args, **options):
        # Get all Art objects
        arts = Art.objects.select_related('collection__artist').all()
        
        synced_count = 0
        for art in arts:
            # Try to find existing Artwork or create new one
            artwork, created = Artwork.objects.get_or_create(
                title=art.title,
                artist=art.collection.artist,
                defaults={
                    'medium': art.medium,
                    'year_created': art.year_created,
                    'width_cm': art.width_cm,
                    'height_cm': art.height_cm,
                    'image': art.image,
                    'is_available': True,
                    # Set a default price if needed
                    'price': art.physical_price or art.digital_price or 99.99,
                    'currency': 'USD'
                }
            )
            
            if not created:
                # Update existing Artwork
                artwork.medium = art.medium
                artwork.year_created = art.year_created
                artwork.width_cm = art.width_cm
                artwork.height_cm = art.height_cm
                artwork.image = art.image
                artwork.is_available = True
                if not artwork.price:
                    artwork.price = art.physical_price or art.digital_price or 99.99
                artwork.save()
            
            synced_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully synced {synced_count} artworks and made them available'
            )
        )