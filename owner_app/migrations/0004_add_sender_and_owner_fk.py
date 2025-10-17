"""
Migration to add sender and owner ForeignKey fields to Messages (nullable).
"""
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0003_add_unread_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(
                related_name='sent_messages',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='messages',
            name='owner',
            field=models.ForeignKey(
                related_name='received_messages',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                blank=True,
            ),
        ),
    ]
