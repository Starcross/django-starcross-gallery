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
import os
import piexif


class Image(models.Model):

    data = models.ImageField(upload_to=settings.GALLERY_IMAGES_PATH)
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
    date_taken = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._date_taken = None # default will use upload time (mtime)
        # See if we can set _date_taken:
        if not 'data' in kwargs: return
        img = pImage.open(kwargs['data'].file)
        if not img.info.get('exif'): return
        edata = piexif.load(img.info['exif'])
        if not edata.get('Exif'): return
        dt_original = edata['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        if not dt_original: return
        self._date_taken = datetime.strptime(dt_original.decode(),"%Y:%m:%d %H:%M:%S")


    def save(self, *args, **kwargs):
        # The first save commits the uploaded file and creates self.data.file
        super().save(*args, **kwargs)
        # Pre-set date_taken: get exif date if exif exists and save to allow db
        # queries, and admin overrides
        if not self.date_taken: # Only after the first save
            self.date_taken = self._date_taken \
                if hasattr(self, '_date_taken') and self._date_taken \
                   else self.mtime
            kwargs.update({'force_insert':False, 'force_update':True})
            super().save(*args, **kwargs)

    @cached_property
    def size_str(self):
        if not hasattr(self, 'width'):
            try:
                with pImage.open(self.data.path) as img:
                    self.width = img.width
                    self.height = img.height
                    img.close()
            except (ValueError,):
                # storage/cache seems to have not been created yet,
                # this happens only on first admin pImage.open access,
                # ok next time (fixme: sync)
                self.width = 0
                self.height = 0
        return '%d x %d' % (self.width, self.height)

    @cached_property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    @cached_property
    def exif(self):
        """ Retrieve exif data using PIL as a dictionary """
        exif_data = {}
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
    def mtime(self):
        return datetime.fromtimestamp(os.path.getmtime(self.data.path))

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
    published = models.BooleanField(default=True)
    
    class Meta(object):
        ordering = ['-order', '-pk']

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
