"""
Migration to add generic relation fields to Media.

This migration adds ContentType FK and object_id so the Media model's
`content_type`/`object_id` pair exists in the database. It is written
as a safe migration that allows nulls for backward compatibility.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0014_media"),
    ]

    operations = [
        migrations.AddField(
            model_name="media",
            name="content_type",
            field=models.ForeignKey(
                to="contenttypes.ContentType",
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="object_id",
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
