from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0002_contact_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]
