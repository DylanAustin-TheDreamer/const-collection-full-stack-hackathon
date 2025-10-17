from django.contrib import admin
from django.utils.html import format_html
from .models import ArtistProfile, Contact, Messages


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

# Additional admin registrations for Contact and Messages can be
# added similarly


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    
    list_display = ('city', 'email', 'phone')
    search_fields = ('city', 'email')


@admin.register(Messages)
class UserMessages(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'subject', 'owner', 'sender', 'sent_at', 'unread'
    )
    search_fields = ('name', 'email', 'subject')
    list_filter = ('subject', 'owner', 'sent_at', 'unread')
    actions = ['mark_read', 'mark_unread']

    def mark_read(self, request, queryset):
        queryset.update(unread=False)
        cnt = queryset.count()
        self.message_user(request, f'Marked {cnt} messages as read')

    def mark_unread(self, request, queryset):
        queryset.update(unread=True)
        cnt = queryset.count()
        self.message_user(request, f'Marked {cnt} messages as unread')

    mark_read.short_description = 'Mark selected messages as read'
    mark_unread.short_description = 'Mark selected messages as unread'
