from django.db import models


# Add event models here
class exhibition(models.Model):
    exhibition_id = models.IntegerField()

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster_url = models.URLField(max_length=200, null=True, blank=True)
    artist_id = models.IntegerField(null=True, blank=True)