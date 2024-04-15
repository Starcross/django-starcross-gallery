# Handwritten by Ronnie van 't Westeinde (not generated!)
from datetime import datetime
from django.db import migrations
from gallery.models import Image


def create_defaults_for_date_taken_field(apps, schema_editor):
    for image in Image.objects.all():
        # Do the best we can to fill in the date_taken fields during the migration
        if image.date_taken is None:
            try:
                image.date_taken = image.retrieve_date_taken()
            except FileNotFoundError:
                # Use the current time stamp, can be changed if needed in the admin
                image.date_taken = datetime.now()
            image.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_image_date_taken'),
    ]

    operations = [
        migrations.RunPython(create_defaults_for_date_taken_field, reverse_code=migrations.RunPython.noop),
    ]
