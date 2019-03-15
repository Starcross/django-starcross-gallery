from gallery.models import Image, Album
from django.contrib import admin
from imagekit.admin import AdminThumbnail


class ImageAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='data_thumbnail', template='gallery/admin/thumbnail.html')
    list_display = ('title', 'admin_thumbnail', 'date_taken', 'date_uploaded')
    list_filter = ('image_albums',)
    list_per_page = 25
    readonly_fields = ('admin_thumbnail',)


class AlbumAdmin(admin.ModelAdmin):
    filter_horizontal = ('images',)
    raw_id_fields = ('highlight',)


admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)

