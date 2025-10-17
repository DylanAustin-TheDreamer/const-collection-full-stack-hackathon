"""
Generated migration to add Media model.

This file was added manually to create the Media table required for
attaching images/videos/documents to Art and ArtVariant.
"""

from django.db import migrations, models
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('collections_app', '0013_remove_legacy_art_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'file',
                    cloudinary.models.CloudinaryField(
                        blank=True, null=True, resource_type='auto'
                    ),
                ),
                (
                    'media_type',
                    models.CharField(
                        choices=[
                            ('image', 'Image'),
                            ('video', 'Video'),
                            ('pdf', 'Document (PDF)'),
                            ('other', 'Other'),
                        ],
                        default='image',
                        max_length=16,
                    ),
                ),
                ('caption', models.CharField(blank=True, max_length=255)),
                (
                    'is_primary',
                    models.BooleanField(
                        default=False,
                        help_text='Primary media to represent the artwork',
                    ),
                ),
                ('ordering', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'art',
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='media',
                        to='collections_app.art',
                    ),
                ),
                (
                    'variant',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name='media',
                        to='collections_app.artvariant',
                    ),
                ),
            ],
            options={
                'ordering': ['ordering', '-created_at'],
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
            },
        ),
    ]
