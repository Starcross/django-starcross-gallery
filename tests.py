from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import os

from gallery.models import Album


class ImageTests(TestCase):

    test_image_title = "Test Image"
    test_album_title = "My First Album"

    def setUp(self):

        # Find the local directory and add the test media location
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'tests/media/')

        # Create test album with test image inside
        self.album = Album.objects.create(title=self.test_album_title)
        self.image = self.album.images.create(title=self.test_image_title,
                                              data='test_image.jpg')

    # Test global image list
    def test_image_list(self):

        response = self.client.get(reverse('gallery:image_list'))
        self.assertContains(response, self.test_image_title)

    # Test album and auto highlight
    def test_album_list(self):

        response = self.client.get(reverse('gallery:album_list'))

        self.assertContains(response, self.test_album_title)
        image = self.album.images.earliest('id')
        self.assertContains(response, image.data_thumbnail.url)

    # Check empty albums do not cause errors
    def test_empty_album(self):

        self.empty_album = Album.objects.create(title='Empty album')
        response = self.client.get(reverse('gallery:album_list'))
        self.assertEqual(response.status_code, 200)

