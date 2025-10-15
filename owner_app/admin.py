from django.contrib import admin
from django.utils.html import format_html
from .models import ArtistProfile


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'image_preview')
    search_fields = ('name', 'email')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />', obj.image.url
            )
        return ''

    image_preview.short_description = 'Image'
