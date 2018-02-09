from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Image resize defaults
thumbnail_size = 200
preview_size = 1000


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=250)
    data = models.ImageField(upload_to='images')
    data_thumbnail = ImageSpecField(source='data',
                                    processors=[ResizeToFit(width=thumbnail_size, height=thumbnail_size)],
                                    format='JPEG',
                                    options={'quality': 60})
    data_preview = ImageSpecField(source='data',
                                  processors=[ResizeToFit(width=preview_size, height=preview_size)],
                                  format='JPEG',
                                  options={'quality': 60})
    date_uploaded = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)

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
