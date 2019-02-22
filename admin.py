from django.contrib import admin
from gallery.models import Image, Album

# Gallery
admin.site.register(Image)
admin.site.register(Album)
