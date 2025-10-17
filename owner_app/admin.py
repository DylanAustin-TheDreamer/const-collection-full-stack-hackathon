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

# Additional admin registrations for Contact and Messages can be added similarly
class ContactAdmin(admin.ModelAdmin):
    list_display = ('city', 'email', 'phone')
    search_fields = ('city', 'email')

class UserMessages(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('subject', 'sent_at')
