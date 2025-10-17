from django.contrib import admin
from django.utils.html import format_html
from .models import Collection, Art


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = ('name', 'artist', 'cover_preview')
    search_fields = ('name', 'artist__name')
    list_filter = ('artist',)
    list_display_links = ('name',)
    inlines = []

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />',
                obj.cover_image.url,
            )
        return ''

    cover_preview.short_description = 'Cover'


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'collection',
        'year_created',
        'is_available',
        'price',
        'is_featured',
        'image_preview',
    )
    search_fields = ('title', 'collection__name')
    list_filter = ('collection',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />',
                obj.image.url,
            )
        return ''

    image_preview.short_description = 'Image'


# Inline so admins can add Art from a Collection page
class ArtInline(admin.TabularInline):
    model = Art
    extra = 1
    fields = ('title', 'image', 'is_available', 'price')


# Attach the inline to the CollectionAdmin dynamically to avoid
# import order issues
CollectionAdmin.inlines = [ArtInline]
