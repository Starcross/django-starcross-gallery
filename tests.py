from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
import os

from gallery.models import Image

# Create your tests here.

class ImageTests(TestCase):

    test_title = "My new Image"

    def setUp(self):

        # Find the local directory and add the test media location
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, 'tests/media/')

        self.image  = Image.objects.create(title=self.test_title,
                                           data='test_image.jpg')
    # Test global image list
    def test_gallery_list(self):

        response = self.client.get(reverse('gallery:image_list'))

        self.assertContains(response,self.test_title)


