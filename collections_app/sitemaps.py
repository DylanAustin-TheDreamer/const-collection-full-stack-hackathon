from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return [
            'collections_app:index',
            'collections_app:gallery',
            'collections_app:gallery_debug',
            'collections_app:artwork_list',
            'collections_app:featured_artworks',
            'collections_app:manage_media',
            'collections_app:add_media',
            'collections_app:basket',
            'collections_app:checkout',
            'collections_app:user_dashboard',
            'collections_app:messages',
        ]

    def location(self, item):
        return reverse(item)

