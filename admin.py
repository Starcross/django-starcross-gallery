from gallery.models import Image, Album
from django.contrib import admin
from imagekit.admin import AdminThumbnail
# Support adminsortable2 optionally
import importlib
if importlib.util.find_spec('adminsortable2', 'admin'):
    from adminsortable2.admin import SortableAdminMixin
else:
    # Mock up class for mixin
    class SortableAdminMixin:
        mock = True


class ImageAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='data_thumbnail', template='gallery/admin/thumbnail.html')
    list_display = ('title', 'admin_thumbnail', 'date_taken', 'date_uploaded')
    list_filter = ('image_albums',)
    list_per_page = 25
    readonly_fields = ('admin_thumbnail',)


class AlbumAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ['-order']
    
    list_display = ('title', 'published', 'order', 'order_number')
    list_display_links = ('title',)
    if hasattr(SortableAdminMixin, 'mock'):
        list_editable = ('order',)
        list_display = ('title', 'published', 'order')
    filter_horizontal = ('images',)
    raw_id_fields = ('highlight',)

    @admin.display(description='order#')
    def order_number(self, album):
        return album.order

admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)


