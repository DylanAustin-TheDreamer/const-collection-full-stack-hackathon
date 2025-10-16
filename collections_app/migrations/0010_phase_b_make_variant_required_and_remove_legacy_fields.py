from django.db import migrations, models
import django.db.models.deletion


def backfill_variant(apps, schema_editor):
    Art = apps.get_model('collections_app', 'Art')
    ArtVariant = apps.get_model('collections_app', 'ArtVariant')
    BasketItem = apps.get_model('collections_app', 'BasketItem')

    # Find or create a global fallback variant if none exist
    first_variant = ArtVariant.objects.first()
    if not first_variant:
        first_art = Art.objects.first()
        if first_art:
            medium_choice = getattr(ArtVariant, 'ORIGINAL', 'original_piece')
            first_variant = ArtVariant.objects.create(
                art=first_art,
                medium=medium_choice,
                is_available=getattr(first_art, 'is_available', False),
                price=(getattr(first_art, 'price', None) or 0),
                currency=(getattr(first_art, 'currency', 'USD') or 'USD'),
            )

    # Best-effort: assign a variant for any BasketItem missing one
    for item in (
        BasketItem.objects.select_related('art').filter(variant__isnull=True)
    ):
        chosen = None
        art = getattr(item, 'art', None)
        if art:
            variants = ArtVariant.objects.filter(art=art)
            original_medium = getattr(ArtVariant, 'ORIGINAL', 'original_piece')
            chosen = variants.filter(
                medium=original_medium, is_available=True
            ).first()
            if not chosen:
                chosen = variants.filter(is_available=True).first()
            if not chosen:
                chosen = variants.first()

        if not chosen:
            chosen = first_variant

        if chosen:
            item.variant_id = chosen.pk
            if not getattr(item, 'price_at_addition', None):
                art_price = getattr(getattr(item, 'art', None), 'price', None)
                item.price_at_addition = (
                    getattr(chosen, 'price', None) or art_price or 0
                )
            item.save()


def noop_reverse(apps, schema_editor):
    # Not reversible in general
    return


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0009_orderitem_variant_id_orderitem_variant_medium"),
    ]

    operations = [
        migrations.RunPython(backfill_variant, noop_reverse),

        migrations.AlterField(
            model_name="basketitem",
            name="variant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="basket_items",
                to="collections_app.artvariant",
                null=False,
            ),
        ),

        migrations.RemoveField(model_name="art", name="physical_available"),
        migrations.RemoveField(model_name="art", name="digital_available"),
        migrations.RemoveField(model_name="art", name="physical_price"),
        migrations.RemoveField(model_name="art", name="digital_price"),
    ]
from django.db import migrations, models
import django.db.models.deletion


def backfill_variant(apps, schema_editor):
    Art = apps.get_model('collections_app', 'Art')
    ArtVariant = apps.get_model('collections_app', 'ArtVariant')
    BasketItem = apps.get_model('collections_app', 'BasketItem')

    # Find a global fallback variant if repository has no variants
    first_variant = ArtVariant.objects.first()
    if not first_variant:
        first_art = Art.objects.first()
        if first_art:
            medium_choice = getattr(ArtVariant, 'ORIGINAL', 'original_piece')
            first_variant = ArtVariant.objects.create(
                art=first_art,
                medium=medium_choice,
                is_available=getattr(first_art, 'is_available', False),
                price=(getattr(first_art, 'price', None) or 0),
                currency=(getattr(first_art, 'currency', 'USD') or 'USD'),
            )

    # Best-effort: assign a variant to any BasketItem missing one
    qs = BasketItem.objects.select_related('art').filter(variant__isnull=True)
    for item in qs:
        chosen = None
        art = getattr(item, 'art', None)
        if art:
            variants = ArtVariant.objects.filter(art=art)
            original_medium = getattr(ArtVariant, 'ORIGINAL', 'original_piece')
            # prefer available original, then any available, then first
            chosen = variants.filter(
                medium=original_medium, is_available=True
            ).first()
            if not chosen:
                chosen = variants.filter(is_available=True).first()
            if not chosen:
                chosen = variants.first()

        if not chosen:
            chosen = first_variant

        if chosen:
            item.variant_id = chosen.pk
            if not getattr(item, 'price_at_addition', None):
                art_price = getattr(getattr(item, 'art', None), 'price', None)
                item.price_at_addition = (
                    getattr(chosen, 'price', None) or art_price or 0
                )
            item.save()


def noop_reverse(apps, schema_editor):
    # No reliable reverse: leave as a no-op
    return


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0009_orderitem_variant_id_orderitem_variant_medium"),
    ]

    operations = [
        migrations.RunPython(backfill_variant, noop_reverse),

        migrations.AlterField(
            model_name="basketitem",
            name="variant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="basket_items",
                to="collections_app.artvariant",
                null=False,
            ),
        ),

        migrations.RemoveField(model_name="art", name="physical_available"),
        migrations.RemoveField(model_name="art", name="digital_available"),
        migrations.RemoveField(model_name="art", name="physical_price"),
        migrations.RemoveField(model_name="art", name="digital_price"),
    ]
from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Art = apps.get_model('collections_app', 'Art')
    ArtVariant = apps.get_model('collections_app', 'ArtVariant')
    BasketItem = apps.get_model('collections_app', 'BasketItem')

    # Find or create a global fallback variant to use when an Art
    # has no variants
    first_variant = ArtVariant.objects.first()
    if not first_variant:
        first_art = Art.objects.first()
        if first_art:
            medium_choice = (
                ArtVariant.ORIGINAL
                if hasattr(ArtVariant, 'ORIGINAL')
                else 'original_piece'
            )
            first_variant = ArtVariant.objects.create(
                art=first_art,
                medium=medium_choice,
                is_available=getattr(first_art, 'is_available', False),
                price=(getattr(first_art, 'price', None) or 0),
                currency=(getattr(first_art, 'currency', 'USD') or 'USD'),
            )

    # Backfill BasketItem.variant for items missing it
    for item in (
        BasketItem.objects.select_related('art')
        .filter(variant__isnull=True)
    ):
        target_variant = None
        art = getattr(item, 'art', None)
        if art:
            # Prefer an available ORIGINAL variant, then any available,
            # then any variant
            variants = ArtVariant.objects.filter(art=art)
            target_variant = (
                variants.filter(medium='original_piece', is_available=True)
                .first()
            )
            if not target_variant:
                target_variant = variants.filter(is_available=True).first()
            if not target_variant:
                target_variant = variants.first()

        if not target_variant:
            target_variant = first_variant

        if target_variant:
            # set variant and snapshot price
            item.variant_id = target_variant.pk
            if not getattr(item, 'price_at_addition', None):
                art_price = getattr(getattr(item, 'art', None), 'price', None)
                item.price_at_addition = (
                    getattr(target_variant, 'price', None) or art_price or 0
                )
            item.save()


def backwards(apps, schema_editor):
    # We can't reliably restore removed fields; leave a no-op for
    # reverse migration.
    return


class Migration(migrations.Migration):

    dependencies = [
        (
            'collections_app',
            '0009_orderitem_variant_id_orderitem_variant_medium',
        ),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),

        # Ensure variant is non-nullable and protected at DB level
        migrations.AlterField(
            model_name='basketitem',
            name='variant',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='basket_items',
                to='collections_app.artvariant',
            ),
        ),

        # Remove legacy per-medium fields from Art now that variants are
        # the source of truth
        migrations.RemoveField(
            model_name='art',
            name='physical_available',
        ),
        migrations.RemoveField(
            model_name='art',
            name='digital_available',
        ),
        migrations.RemoveField(
            model_name='art',
            name='physical_price',
        ),
        migrations.RemoveField(
            model_name='art',
            name='digital_price',
        ),
    ]
