from django.contrib import admin
from django.utils.html import format_html
from .models import Exhibition, ExhibitionArt


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'start_date',
        'end_date',
        'location',
        'status',
        'cover_preview',
    )
    search_fields = ('title',)

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />',
                obj.cover_image.url,
            )
        return ''

    cover_preview.short_description = 'Cover'


@admin.register(ExhibitionArt)
class ExhibitionArtAdmin(admin.ModelAdmin):

    list_display = ('exhibition', 'art')
    search_fields = ('exhibition__title', 'art__title')
