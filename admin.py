from django.contrib import admin
from gallery.models import Image, Album, Tag

# Register your models here.

# Gallery
admin.site.register(Image)
admin.site.register(Album)
admin.site.register(Tag)