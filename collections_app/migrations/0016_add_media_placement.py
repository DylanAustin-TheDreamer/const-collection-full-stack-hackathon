"""
Add the `placement` field to Media.

Some environments were missing this column which caused a ProgrammingError
when querying the Media table. This migration adds the field with a default
value and allows nulls to remain safe for existing rows.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0015_add_media_content_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="media",
            name="placement",
            field=models.CharField(
                max_length=32,
                choices=[
                    ("art", "Artwork"),
                    ("homepage", "Homepage"),
                    ("collection", "Collection"),
                    ("artist", "Artist"),
                    ("page", "Custom Page"),
                ],
                default="art",
            ),
        ),
    ]
