from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils.datastructures import MultiValueDict
import os
from datetime import datetime

from gallery.models import Album, Image
from gallery.forms import ImageCreateForm


class ImageTests(TestCase):

    test_image_title = "Test Image"
    test_album_title = "My First Album"

    image_filename = 'test_image.jpg'

    exif_data = ['Sony  DSLR-A700', 'F/11.0', '1/500s', '16mm', 'ISO 200']

    def setUp(self):

        # Find the local directory and add the test media location
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'tests/media/')

        # Create test album with test image inside
        self.album = Album.objects.create(title=self.test_album_title)
        self.image = self.album.images.create(title=self.test_image_title,
                                              data=self.image_filename)

    # Test global image list
    def test_image_list(self):

        response = self.client.get(reverse('gallery:image_list'))
        self.assertContains(response, self.test_image_title, msg_prefix="Image data missing from image feed")

    # Test image preview
    def test_image_detail(self):

        response = self.client.get(reverse('gallery:image_detail',
                                           kwargs={'pk': self.image.pk, 'slug': self.image.title}))
        self.assertContains(response, self.test_image_title, msg_prefix="Image preview does not contain image data")
        # Check exif data present
        for data in self.exif_data:
            self.assertContains(response, data, msg_prefix="Exif data missing")
        # Check image's album appears in this context
        self.assertContains(response, self.test_album_title, count=2, msg_prefix="Image preview does not related album")

    # Test image preview with album context. Should contain previews to any other images in the same album
    def test_album_image_detail(self):
        response = self.client.get(reverse('gallery:album_image_detail',
                                           kwargs={'pk': self.image.pk, 'slug': self.image.title,
                                                   'apk': self.album.pk}))
        self.assertContains(response, self.test_album_title, count=2, msg_prefix="Image preview incorrect")

    # Test album and auto highlight
    def test_album_list(self):

        response = self.client.get(reverse('gallery:album_list'))

        self.assertContains(response, self.test_album_title, msg_prefix="Album data missing from album list")
        image = self.album.images.earliest('id')
        self.assertContains(response, image.data_thumbnail.url, msg_prefix="Album list missing album url")

    # Check empty albums do not cause errors
    def test_empty_album(self):

        self.empty_album = Album.objects.create(title='Empty album')
        response = self.client.get(reverse('gallery:album_list'))
        self.assertEqual(response.status_code, 200, "Error displaying empty album")

    def test_image_properties(self):

        image = Image.objects.all()[0]
        self.assertEqual(image.title, ImageTests.test_image_title, "Incorrect title in image object")
        self.assertEqual(image.date_taken, datetime.strptime("2013-03-21 15:04:53", "%Y-%m-%d %H:%M:%S"),
                         "Incorrect date in image object")
        self.assertEqual(image.slug, "test-image", "Incorrect slug in image object")

    def test_image_create_form(self):
        data = {'apk': self.album.pk}
        image_path = os.path.join(settings.MEDIA_ROOT, self.image_filename)
        image_files = MultiValueDict({'data': [image_path]})
        form = ImageCreateForm(data, files=image_files)
        form.clean()



