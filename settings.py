from django.conf import settings

# Image resize defaults

# Target height for thumbnail display
GALLERY_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_THUMBNAIL_SIZE', 250)
# Large preview in modal popup, enough to fill a typical browser window
GALLERY_PREVIEW_SIZE = getattr(settings, 'GALLERY_PREVIEW_SIZE', 1000)
# JPEG encoding quality
GALLERY_RESIZE_QUALITY = getattr(settings, 'GALLERY_RESIZE_QUALITY', 80)


