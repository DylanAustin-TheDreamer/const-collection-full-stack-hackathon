"""
Add hero/second_section/third_section boolean flags to Media and make
art nullable (SET_NULL). Also add conditional unique constraints so only
one Media row can be hero/second_section/third_section at a time.
"""

from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("collections_app", "0016_add_media_placement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="art",
            field=models.ForeignKey(
                to="collections_app.Art",
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name='media',
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="hero",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="media",
            name="second_section",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="media",
            name="third_section",
            field=models.BooleanField(default=False),
        ),
        # Add conditional unique constraints for Django-supported DBs (Postgres)
        migrations.AddConstraint(
            model_name='media',
            constraint=models.UniqueConstraint(
                fields=['hero'],
                name='unique_hero_true',
                condition=Q(hero=True),
            ),
        ),
        migrations.AddConstraint(
            model_name='media',
            constraint=models.UniqueConstraint(
                fields=['second_section'],
                name='unique_second_true',
                condition=Q(second_section=True),
            ),
        ),
        migrations.AddConstraint(
            model_name='media',
            constraint=models.UniqueConstraint(
                fields=['third_section'],
                name='unique_third_true',
                condition=Q(third_section=True),
            ),
        ),
    ]
