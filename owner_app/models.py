from django.db import models
from cloudinary.models import CloudinaryField


class ArtistProfile(models.Model):
    # Unique ID (auto PK by Django)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    image = CloudinaryField(resource_type='image', blank=True, null=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

    class Meta:
        verbose_name = 'Artist Profile'
        verbose_name_plural = 'Artist Profiles'


class Contact(models.Model):
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    curator_name = models.CharField(max_length=200, blank=True)
    curator_email = models.EmailField(blank=True)
    opening_hours = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.city} <{self.email}>"

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'


class Messages(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    subject = models.CharField(
        max_length=20,
        choices=[
            ('general', 'General Inquiry'),
            ('artwork', 'Artwork Purchase'),
            ('exhibition', 'Exhibition Information'),
        ],
        default='general'
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

