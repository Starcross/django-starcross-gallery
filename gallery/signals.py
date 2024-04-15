from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from gallery.models import Image


# Delete image files from disk when image objects are deleted
@receiver(post_delete, sender=Image)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    instance.data.delete(save=False)


@receiver(post_save, sender=Image)
def save_image(sender, instance, **kwargs):
    if instance.date_taken is None:
        instance.date_taken = instance.retrieve_date_taken()
