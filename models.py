from functools import reduce

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, Transpose as KitTranspose
from PIL import Image as pImage
from PIL.ExifTags import TAGS, Base
from gallery import settings
from pathlib import Path
from datetime import datetime
import os


class Transpose(KitTranspose):
    """Override the default Transpose processor to call getexif instead of _getexif
    Pending https://github.com/matthewwithanm/pilkit/pull/80/changes/c25a349c45e922b299e2eaf21e1a7eb80e9b2931"""

    def process(self, img):
        if self.AUTO in self.methods:
            try:
                orientation = img.getexif()[0x0112]
                ops = self._EXIF_ORIENTATION_STEPS[orientation]
            except (IndexError, KeyError, TypeError, AttributeError):
                ops = []
        else:
            ops = self.methods
        for method in ops:
            img = img.transpose(method)
        return img


class Image(models.Model):

    data = models.ImageField(upload_to=settings.GALLERY_IMAGES_PATH)
    data_thumbnail = ImageSpecField(
        source='data',
        processors=[
            Transpose(Transpose.AUTO),
            ResizeToFit(
                height=settings.GALLERY_THUMBNAIL_SIZE * settings.GALLERY_HDPI_FACTOR
            ),

        ],
        format='JPEG',
        options={'quality': settings.GALLERY_RESIZE_QUALITY},
    )
    data_preview = ImageSpecField(
        source='data',
        processors=[
            Transpose(Transpose.AUTO),
            ResizeToFit(
                width=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR,
                height=settings.GALLERY_PREVIEW_SIZE * settings.GALLERY_HDPI_FACTOR
            ),

        ],
        format='JPEG',
        options={'quality': settings.GALLERY_RESIZE_QUALITY},
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)

    @cached_property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    @cached_property
    def exif(self):
        """ Retrieve exif data using PIL and build a dictionary"""
        exif_data = {}
        with pImage.open(self.data) as img:
            # Extract standard EXIF data (including IFD0 and Exif Sub-IFD)
            if hasattr(img, 'getexif'):
                exif_obj = img.getexif()
                if exif_obj:
                    info = dict(exif_obj)
                    info.update(exif_obj.get_ifd(Base.ExifOffset))

                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        exif_data[decoded] = value

            # Extract XMP metadata (for Copyright, Title, Description, etc. for use in LD-JSON)
            if hasattr(img, 'getxmp'):
                xmp_data = img.getxmp()
                if xmp_data and 'xmpmeta' in xmp_data:
                    try:
                        # Navigate through the standard XMP structure: xmpmeta -> RDF -> Description
                        rdf = xmp_data['xmpmeta']['RDF']['Description']
                        # There may be multiple description entries which would return a list
                        if type(rdf) is list:
                            rdf = reduce(lambda acc, curr: acc | curr, rdf)
                        if 'WebStatement' in rdf:
                            exif_data["License"] = rdf['WebStatement']
                        if 'rights' in rdf and not 'Copyright' in exif_data:
                            exif_data['Copyright'] = rdf['rights']['Alt']['li']['text']
                        if 'creator' in rdf:
                            exif_data['Creator'] = rdf['creator']['Seq']['li']
                        if 'title' in rdf:
                            exif_data['Title'] = rdf['title']['Alt']['li']['text']
                        if 'description' in rdf:
                            exif_data['Description'] = rdf['description']['Alt']['li']['text']
                        if 'subject' in rdf:
                            exif_data["Subject"] = rdf['subject']['Bag']['li']
                    except (KeyError, TypeError):
                        # Fail silently if the expected XMP structure isn't as assumed
                        pass

            # Process camera data for easy rendering in-template
            exif_data['Camera'] = exif_data.get('Model', '')
            if exif_data.get('Make', '') not in exif_data['Camera']:  # Work around for Canon
                exif_data['Camera'] = "{0} {1}".format(exif_data['Make'].title(), exif_data['Model'])
            if 'FNumber' in exif_data:
                exif_data['Aperture'] = str(exif_data['FNumber'].numerator / exif_data['FNumber'].denominator)
            if 'ExposureTime' in exif_data:
                exif_data['Exposure'] = "{0}/{1}".format(exif_data['ExposureTime'].numerator,
                                                         exif_data['ExposureTime'].denominator)

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

    class Meta(object):
        ordering = ['order', '-pk']

    @property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    @property
    def display_highlight(self):
        """ User-selectable thumbnail for the album """
        if self.highlight :
            image = self.highlight
        # if there is no highlight but there are images in the album, use the first
        else:
            image = self.images.earliest('id')
        if image:
            image.title = self.title  # use the album title instead of the highlight title
        return image

    def get_absolute_url(self):
        return reverse('gallery:album_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title
