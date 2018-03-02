from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from gallery import settings
from PIL import Image as pImage
from PIL.ExifTags import TAGS


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Image(models.Model):

    title = models.CharField(max_length=250)
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
    def exif(self):
        exif_dict = {}
        img = pImage.open(self.data)
        info = img._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_dict[decoded] = value
        return exif_dict

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

    def __str__(self):
        return self.title
