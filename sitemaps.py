from django.contrib.sitemaps import Sitemap
from gallery.models import Image


class ImageSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Image.objects.all()

    def lastmod(self, item: Image):
        return item.mtime

