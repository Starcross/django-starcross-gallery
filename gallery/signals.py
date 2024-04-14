from django.dispatch import receiver
from django.db.models.signals import post_delete

from gallery.models import Image


# Delete image files from disk when image objects are deleted
@receiver(post_delete, sender=Image)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    instance.data.delete(save=False)
