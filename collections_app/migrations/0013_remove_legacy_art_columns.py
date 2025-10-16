from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0011_alter_basketitem_variant"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE collections_app_art "
                "DROP COLUMN IF EXISTS physical_available, "
                "DROP COLUMN IF EXISTS digital_available, "
                "DROP COLUMN IF EXISTS physical_price, "
                "DROP COLUMN IF EXISTS digital_price;"
            ),
            reverse_sql=(
                "ALTER TABLE collections_app_art "
                "ADD COLUMN physical_available boolean NOT NULL DEFAULT false, "
                "ADD COLUMN digital_available boolean NOT NULL DEFAULT false, "
                "ADD COLUMN physical_price numeric NULL, "
                "ADD COLUMN digital_price numeric NULL;"
            ),
        )
    ]
