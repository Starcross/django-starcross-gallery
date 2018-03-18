from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from PIL import Image as pImage
from PIL.ExifTags import TAGS
from gallery import settings
from pathlib import Path

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Image(models.Model):

    data = models.ImageField(upload_to='images')
    data_thumbnail = ImageSpecField(source='data',
                                    processors=[ResizeToFit(height=settings.GALLERY_THUMBNAIL_SIZE * 2)],
                                    format='JPEG',
                                    options={'quality': settings.GALLERY_RESIZE_QUALITY})
    data_preview = ImageSpecField(source='data',
                                  processors=[ResizeToFit(width=settings.GALLERY_PREVIEW_SIZE,
                                                          height=settings.GALLERY_PREVIEW_SIZE)],
                                  format='JPEG',
                                  options={'quality': settings.GALLERY_RESIZE_QUALITY})
    date_uploaded = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def exif(self):
        exif_dict = {}
        img = pImage.open(self.data)
        info = img._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_dict[decoded] = value
        return exif_dict

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
    images = models.ManyToManyField(Image, blank=True)
    highlight = models.OneToOneField(Image,
                                     related_name='album_highlight',
                                     null=True, blank=True,
                                     on_delete=models.PROTECT
                                     )

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title
