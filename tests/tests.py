from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

import os
from datetime import datetime

from gallery.models import Album, Image
from gallery.forms import ImageCreateForm


class ImageTests(TestCase):
    """ Test case for starcross-django-gallery """

    test_image_title = "Antibes Marina"
    test_slug = "antibes-marina"
    test_album_title = "My First Album"
    test_image_title_unicode = "Паровоз"

    image_filenames = ['Antibes_Marina.jpg', 'Castle_Combe.jpg', 'Паровоз.jpg']

    exif_data = ['Sony  DSLR-A700', 'F/11.0', '1/500s', '16mm', 'ISO 200']

    username = 'admin'
    password = 'yj4KlZ6N'

    def setUp(self):

        # Find the local directory and add the test media location
        test_root = os.path.abspath(os.path.dirname(__file__))
        settings.MEDIA_ROOT = os.path.join(test_root, 'media/')

        # Create test album with test images inside
        self.album = Album.objects.create(title=self.test_album_title)
        self.images = []
        for filename in self.image_filenames:
            self.images += [self.album.images.create(data=filename)]
        self.image = self.images[0]  # Set main set image
        self.unicode_image = self.images[2]  # Set unicode image

        User.objects.create_superuser(self.username, 'user@email.com', self.password)
        self.client.login(username=self.username, password=self.password)

    def test_image_list(self):
        """ Test global image list """

        response = self.client.get(reverse('gallery:image_list'))
        self.assertContains(response, self.test_image_title, msg_prefix="Image title missing from image feed")
        self.assertContains(response, self.test_image_title_unicode,
                            msg_prefix="Unicode image title missing from image feed")

    def test_image_detail(self):
        """ Test image preview """

        response = self.client.get(reverse('gallery:image_detail',
                                           kwargs={'pk': self.image.pk, 'slug': self.image.title}))
        self.assertContains(response, self.test_image_title, msg_prefix="Image preview does not contain image title")
        # Check exif data present
        for data in self.exif_data:
            self.assertContains(response, data, msg_prefix="Exif data missing")
        # Check image's album appears in this context
        self.assertContains(response, self.test_album_title, count=2,
                            msg_prefix="Image preview does not contain related album")

    def test_album_image_detail(self):
        """ Test image preview with album context. Should contain previews to any other images in the same album """
        response = self.client.get(reverse('gallery:album_image_detail',
                                           kwargs={'pk': self.image.pk, 'slug': self.image.title,
                                                   'apk': self.album.pk}))
        self.assertContains(response, self.test_album_title, count=2, msg_prefix="Image preview incorrect")

    def test_album_list(self):
        """ Test album and auto highlight """
        response = self.client.get(reverse('gallery:album_list'))

        self.assertContains(response, self.test_album_title, msg_prefix="Album data missing from album list")
        image = self.album.images.earliest('id')
        self.assertContains(response, image.data_thumbnail.url, msg_prefix="Album list missing album url")

    def test_empty_album(self):
        """ Check empty albums do not cause errors """

        self.empty_album = Album.objects.create(title='Empty album')
        response = self.client.get(reverse('gallery:album_list'))
        self.assertEqual(response.status_code, 200, "Error displaying empty album")
        Album.objects.all().last().delete()

    def test_album_view(self):
        """ Test albums contain images """

        response = self.client.get(reverse('gallery:album_detail',
                                   kwargs={'pk': self.album.pk, 'slug': self.album.title}))
        self.assertEqual(response.status_code, 200, "Error testing album view")
        self.assertContains(response, self.image.title, count=2, msg_prefix="Error testing image in album view")

    def test_image_properties(self):
        image = Image.objects.all()[0]
        self.assertEqual(image.title, ImageTests.test_image_title, "Incorrect title in image object")
        self.assertEqual(image.date_taken, datetime.strptime("2013-03-21 15:04:53", "%Y-%m-%d %H:%M:%S"),
                         "Incorrect date in image object")
        self.assertEqual(image.slug, self.test_slug, "Incorrect slug in image object")

    def test_valid_image_upload(self):
        album_size = len(self.album.images.all())
        image_path = os.path.join(settings.MEDIA_ROOT, self.image_filenames[0])

        with open(image_path, 'rb') as image_file:
            data = {'apk': self.album.pk,
                    'data': image_file}
            response = self.client.post(reverse('gallery:image_upload'), data=data)
        self.assertRedirects(response, reverse('gallery:image_list'), msg_prefix="Error uploading image")
        self.assertEqual(album_size + 1, len(self.album.images.all()), "Error uploading image to album")
        self.album.images.last().delete()
        self.assertEqual(album_size, len(self.album.images.all()), "Error removing image")

    def test_empty_image_upload(self):
        response = self.client.post(reverse('gallery:image_upload'))
        self.assertContains(response, "Unable to add")

    def test_invalid_image_upload(self):
        data = {'data': SimpleUploadedFile('text.txt', b'text')}
        response = self.client.post(reverse('gallery:image_upload'), data=data)
        self.assertContains(response, "Unable to add invalid image", msg_prefix="Error testing invalid image data")

    def test_image_modified_time(self):
        self.assertIsInstance(self.image.mtime, datetime)