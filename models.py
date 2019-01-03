from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from PIL import Image as pImage
from PIL.ExifTags import TAGS
from gallery import settings
from pathlib import Path
from datetime import datetime
import os


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Image(models.Model):

    data = models.ImageField(upload_to='images')
    data_thumbnail = ImageSpecField(source='data',
                                    processors=[ResizeToFit(
                                        height=settings.GALLERY_THUMBNAIL_SIZE * settings.GALLERY_HDPI_FACTOR)],
                                    format='JPEG',
                                    options={'quality': settings.GALLERY_RESIZE_QUALITY})
    data_preview = ImageSpecField(source='data',
                                  processors=[ResizeToFit(width=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR,
                                                          height=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR)],
                                  format='JPEG',
                                  options={'quality': settings.GALLERY_RESIZE_QUALITY})
    date_uploaded = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)

    @cached_property
    def slug(self):
        return slugify(self.title)

    @cached_property
    def exif(self):
        exif_dict = {}
        self.data.open()
        with pImage.open(self.data) as img:
            if hasattr(img, '_getexif'):
                info = img._getexif()
                if not info:
                    return {}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_dict[decoded] = value
        return exif_dict

    @cached_property
    def date_taken(self):
        original_exif = self.exif.get('DateTimeOriginal')
        if not original_exif:
            return self.mtime
        try:
            return datetime.strptime(original_exif, "%Y:%m:%d %H:%M:%S")
        except ValueError:  # Fall back to file modification time
            return self.mtime

    @cached_property
    def mtime(self):
        return datetime.fromtimestamp(os.path.getmtime(self.data.path))

    @property
    def title(self):
        if hasattr(self, '_title'):
            return self._title
        """ Derive a title from the original filename """
        # remove extension
        filename = Path(self.data.name).with_suffix('').name
        # convert spacing characters to whitespaces
        name = filename.translate(str.maketrans('_', ' '))
        # return with first letter caps
        return name.title()

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
    highlight = models.OneToOneField(Image,
                                     related_name='album_highlight',
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL
                                     )

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title
