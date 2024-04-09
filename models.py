from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from PIL import Image as pImage
from PIL.ExifTags import TAGS
from gallery import settings
from pathlib import Path
from datetime import datetime
from django.core.files import storage

# Create storage class and instance, based on the GALLERY_STORAGE setting
# This allows the user the flexibility to use Amazon S3 or any other object storage
# provider. Default is local file storage.
gallery_storage_class = storage.get_storage_class(settings.GALLERY_STORAGE)
gallery_storage = gallery_storage_class()


class Image(models.Model):

    data = models.ImageField(upload_to='images', storage=gallery_storage_class)
    data_thumbnail = ImageSpecField(
        source='data',
        processors=[ResizeToFit(height=settings.GALLERY_THUMBNAIL_SIZE * settings.GALLERY_HDPI_FACTOR)],
        format='JPEG',
        options={'quality': settings.GALLERY_RESIZE_QUALITY}
    )
    data_preview = ImageSpecField(
        source='data',
        processors=[ResizeToFit(
            width=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR,
            height=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR
        )],
        format='JPEG',
        options={'quality': settings.GALLERY_RESIZE_QUALITY}
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)

    @cached_property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    @cached_property
    def exif(self):
        """ Retrieve exif data using PIL as a dictionary """
        exif_data = {}
        self.data.open()
        with pImage.open(self.data) as img:
            if hasattr(img, '_getexif'):
                info = img._getexif()
                if not info:
                    return {}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value
                # Process some data for easy rendering in template
                exif_data['Camera'] = exif_data.get('Model', '')
                if exif_data.get('Make', '') not in exif_data['Camera']:  # Work around for Canon
                    exif_data['Camera'] = "{0} {1}".format(exif_data['Make'].title(), exif_data['Model'])
                if 'FNumber' in exif_data:
                    exif_data['Aperture'] = str(exif_data['FNumber'].numerator / exif_data['FNumber'].denominator)
                if 'ExposureTime' in exif_data:
                    exif_data['Exposure'] = "{0}/{1}".format(exif_data['ExposureTime'].numerator,
                                                             exif_data['ExposureTime'].denominator)
            img.close()
        return exif_data

    @cached_property
    def date_taken(self):
        """ Use the date taken from the exif data, otherwise file modification time """
        original_exif = self.exif.get('DateTimeOriginal')
        if not original_exif:
            return self.mtime
        try:
            return datetime.strptime(original_exif, "%Y:%m:%d %H:%M:%S")
        except ValueError:  # Fall back to file modification time
            return self.mtime

    @cached_property
    def mtime(self):
        # Use the storage class to get the modified time, which works both locally
        # and for remote storage. Translate into zone-unaware datetime to allow
        # comparing with other timestamps
        return gallery_storage.get_modified_time(self.data.name).replace(tzinfo=None)

    @property
    def title(self):
        """ Derive a title from the original filename """
        if hasattr(self, '_title'):
            return self._title
        name = Path(self.data.name)
        # remove extension
        name = name.with_suffix('').name
        # convert spacing characters to whitespaces
        return name.translate(str.maketrans('_', ' '))

    # Temporary override for album highlights
    @title.setter
    def title(self, name):
        self._title = name

    def get_absolute_url(self):
        return reverse('gallery:image_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=250)
    images = models.ManyToManyField(Image, blank=True, related_name='image_albums')
    highlight = models.OneToOneField(
        Image,
        related_name='album_highlight',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['order', '-pk']

    @property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    @property
    def display_highlight(self):
        """ User selectable thumbnail for the album """
        # if there is no highlight but there are images in the album, use the first
        if not self.highlight and self.images.count():
            image = self.images.earliest('id')
        else:
            image = self.highlight
        if image:
            image.title = self.title  # use the album title instead of the highlight title
        return image

    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title
