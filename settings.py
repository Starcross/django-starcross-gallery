from django.conf import settings

# Image resize defaults
GALLERY_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_THUMBNAIL_SIZE', 250)
GALLERY_PREVIEW_SIZE = getattr(settings, 'GALLERY_PREVIEW_SIZE', 1000)
GALLERY_RESIZE_QUALITY = getattr(settings, 'GALLERY_PREVIEW_SIZE', 80)
