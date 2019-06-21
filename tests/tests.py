from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User

import os
from datetime import datetime

from gallery.models import Album, Image
from gallery.forms import ImageCreateForm


class ImageTests(TestCase):

    test_image_title = "Test Image"
    test_album_title = "My First Album"

    image_filename = 'test_image.jpg'

    exif_data = ['Sony  DSLR-A700', 'F/11.0', '1/500s', '16mm', 'ISO 200']

    username = 'admin'
    password = 'yj4KlZ6N'

    def setUp(self):

        # Find the local directory and add the test media location
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'media/')

        # Create test album with test image inside
        self.album = Album.objects.create(title=self.test_album_title)
        self.image = self.album.images.create(title=self.test_image_title,
                                              data=self.image_filename)

        User.objects.create_superuser(self.username, 'user@email.com', self.password)

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

    # Test albums contain images
    def test_album_view(self):

        response = self.client.get(reverse('gallery:album_detail',
                                   kwargs={'pk': self.album.pk, 'slug': self.album.title}))
        self.assertEqual(response.status_code, 200, "Error testing album view")
        self.assertContains(response, self.image.title, count=2, msg_prefix="Error testing image in album view")

    def test_image_properties(self):

        image = Image.objects.all()[0]
        self.assertEqual(image.title, ImageTests.test_image_title, "Incorrect title in image object")
        self.assertEqual(image.date_taken, datetime.strptime("2013-03-21 15:04:53", "%Y-%m-%d %H:%M:%S"),
                         "Incorrect date in image object")
        self.assertEqual(image.slug, "test-image", "Incorrect slug in image object")

    def test_image_form_validation(self):
        data = {'apk': self.album.pk}
        image_path = os.path.join(settings.MEDIA_ROOT, self.image_filename)
        image_files = MultiValueDict({'data': [image_path]})
        form = ImageCreateForm(data, files=image_files)
        form.clean()

    def test_image_upload(self):
        album_size = len(self.album.images.all())
        image_path = os.path.join(settings.MEDIA_ROOT, self.image_filename)
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('gallery:image_upload'))
        self.assertEqual(response.status_code, 200, "Error testing invalid image upload")

        with open(image_path, 'rb') as image_file:
            data = {'apk': self.album.pk,
                    'data': image_file}
            response = self.client.post(reverse('gallery:image_upload'), data=data)
        self.assertRedirects(response, reverse('gallery:image_list'), msg_prefix="Error uploading image")
        self.assertEqual(album_size + 1, len(self.album.images.all()), "Error uploading image to album")
        self.album.images.last().delete()
        self.assertEqual(album_size, len(self.album.images.all()), "Error removing image")

        self.client.logout()
