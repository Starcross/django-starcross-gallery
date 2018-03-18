from django.conf import settings

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = getattr(settings, 'IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY',
                                              'imagekit.cachefiles.strategies.Optimistic')

# Image resize defaults

# Target height for thumbnail display
GALLERY_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_THUMBNAIL_SIZE', 250)
# Large preview in modal popup, enough to fill a typical browser window
GALLERY_PREVIEW_SIZE = getattr(settings, 'GALLERY_PREVIEW_SIZE', 1000)
# JPEG encoding quality
GALLERY_RESIZE_QUALITY = getattr(settings, 'GALLERY_RESIZE_QUALITY', 80)
# Multiple used to increase quality on high resolution screens. Default to double
HDPI_FACTOR = getattr(settings, 'HDPI_FACTOR', 2)
# Image margin as float
IMAGE_MARGIN = getattr(settings, 'IMAGE_MARGIN', 6.0)
