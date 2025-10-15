from django.db import models


# Add your models here.
class Artwork(models.Model):
    artwork_id = models.IntegerField()

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=200, null=True, blank=True)
    medium = models.CharField(max_length=100, null=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('sold', 'Sold')], default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    artist_id = models.IntegerField(null=True, blank=True)
    collection_id = models.IntegerField(null=True, blank=True)