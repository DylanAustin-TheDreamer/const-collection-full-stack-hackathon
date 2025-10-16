from django.core.management.base import BaseCommand
from collections_app.models import Art, Artwork
from decimal import Decimal

class Command(BaseCommand):
    help = 'Syncs Art objects with Artwork objects for store functionality'

    def handle(self, *args, **options):
        # Get all Art objects
        arts = Art.objects.select_related('collection__artist').all()
        
        created_count = 0
        updated_count = 0
        
        for art in arts:
            # Calculate a default price
            default_price = art.physical_price or art.digital_price or Decimal('99.99')
            
            # Try to find or create an Artwork object
            artwork, created = Artwork.objects.get_or_create(
                title=art.title,
                artist=art.collection.artist,
                defaults={
                    'medium': art.medium,
                    'year_created': art.year_created,
                    'width_cm': art.width_cm,
                    'height_cm': art.height_cm,
                    'image': art.image,
                    'price': default_price,
                    'is_available': True,
                    'description': f"From collection: {art.collection.name}"
                }
            )
            
            if created:
                created_count += 1
            else:
                # Update existing artwork
                artwork.medium = art.medium
                artwork.year_created = art.year_created
                artwork.width_cm = art.width_cm
                artwork.height_cm = art.height_cm
                artwork.image = art.image
                artwork.price = default_price
                artwork.is_available = True
                artwork.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully synced {created_count + updated_count} artworks:\n'
                f'- Created: {created_count}\n'
                f'- Updated: {updated_count}'
            )
        )