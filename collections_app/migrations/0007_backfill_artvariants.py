from django.db import migrations


def forwards(apps, schema_editor):
    Art = apps.get_model('collections_app', 'Art')
    ArtVariant = apps.get_model('collections_app', 'ArtVariant')

    for art in Art.objects.all():
        currency = getattr(art, 'currency', None)

        # Original piece -> map from legacy physical_* fields
        try:
            physical_available = getattr(art, 'physical_available')
        except Exception:
            physical_available = False

        if physical_available:
            price = getattr(art, 'physical_price', None) or getattr(art, 'price', None)
            ArtVariant.objects.get_or_create(
                art_id=art.pk,
                medium='original_piece',
                defaults={'is_available': True, 'price': price, 'currency': currency},
            )

        # Digital copy -> map from legacy digital_* fields
        try:
            digital_available = getattr(art, 'digital_available')
        except Exception:
            digital_available = False

        if digital_available:
            price = getattr(art, 'digital_price', None) or getattr(art, 'price', None)
            ArtVariant.objects.get_or_create(
                art_id=art.pk,
                medium='digital_copy',
                defaults={'is_available': True, 'price': price, 'currency': currency},
            )

        # Printed poster is a new medium that can't be reliably inferred from legacy
        # fields. Create a disabled placeholder variant so admins can enable/configure it.
        ArtVariant.objects.get_or_create(
            art_id=art.pk,
            medium='printed_poster',
            defaults={'is_available': False, 'price': None, 'currency': currency},
        )


def backwards(apps, schema_editor):
    ArtVariant = apps.get_model('collections_app', 'ArtVariant')
    # Remove all variants created by the forward migration.
    ArtVariant.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('collections_app', '0006_artvariant'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
