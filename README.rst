.. image:: https://img.shields.io/pypi/v/django-starcross-gallery.svg
    :target: https://pypi.python.org/pypi/django-starcross-gallery/
    :alt: PyPI version

.. image:: https://travis-ci.org/Starcross/django-starcross-gallery.svg?branch=master
    :target: https://travis-ci.org/Starcross/django-starcross-gallery
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/Starcross/django-starcross-gallery/badge.svg?branch=master
    :target: https://coveralls.io/github/Starcross/django-starcross-gallery?branch=master
    :alt: Code coverage

=================
Starcross Gallery
=================

Starcross Gallery is a streamlined photo gallery Django app. Key features are:

* Justified image grid display, as used on sites like Flickr
* Infinite scroll
* Easy drag and drop upload
* Straightforward object model - All metadata is pulled from the file including title and exif data

Demo at http://starcross.eu/gallery

Quick start
-----------

1. Install Starcross gallery using pip::

    pip install django-starcross-gallery

2. Add "gallery" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gallery',
    ]

3. Include the gallery URLconf in your project urls.py like this with your preferred location e.g. "gallery/"::

    path('gallery/', include('gallery.urls')),

4. Ensure a `MEDIA directory <https://docs.djangoproject.com/en/2.1/topics/files/>`_ is set up

5. Run ``python manage.py makemigrations gallery``, then ``python manage.py migrate gallery`` to create the models.

6. Start the development server and create any albums you required in http://127.0.0.1:8000/admin/. It's not necessary to create albums if you prefer just a single image feed

7. Visit http://127.0.0.1:8000/gallery/ to access the gallery. Albums can be added through the django admin interface (/admin)


Instructions
------------

Starcross gallery groups Images into Albums, which enables your to organise your presentation. Add albums via the django admin interface, and drag multiple images into your empty albums in the album page itself. It's also possible to use the gallery as a flat image feed only, which is a view published at <gallery base>/images. All images will be displayed here in descending date order. You can add images here directly as well, but they will not be added to an album.

The gallery was designed with simplicity of Image management in mind, so titles are derived from the file name. You only need to add albums and then drag your collection into place. The idea is to avoid the need to manage your collection both on the website and on your disk. If you wish to reorganise, you can delete and easily re-upload

Images in albums are ordered by the date the photo was taken if available in the exif data, or failing that the modification date

Album order can be specified in the Django admin interface. Support for `django-admin-sortable2 <https://github.com/jrief/django-admin-sortable2>`_ is provided, if you want drag and drop ordering in the admin interface. Just installing the module is all that's required. If you have already added albums you will need to use the `reorder <https://django-admin-sortable2.readthedocs.io/en/latest/usage.html#initial-data>`_ command.

Settings
--------

Override these default settings by adding to your settings.py


**GALLERY_LOGO_PATH** -- Default: "gallery/images/starcross.png"

Path to the header logo within the static directory. If you do not wish to use a logo, override with a blank string

**GALLERY_TITLE** -- Default: "Gallery"

The title of the Gallery shown in the header on the main page and image feed

**GALLERY_FOOTER_INFO** -- Default: "Starcross Gallery"

Information text in the footer

**GALLERY_FOOTER_EMAIL** -- Default: "gallery@starcross.eu"

Contact email address in the footer. Override with a blank string to hide

**GALLERY_THEME_COLOR** -- Default "black"

Use a predefined theme color scheme. Options are black, white, or grey

**GALLERY_THUMBNAIL_SIZE** -- Default: 200

The target thumbnail height in px. This will vary slightly in rendering due to the justified layout

**GALLERY_PREVIEW_SIZE** -- Default: 1000

The preview size in px - width or height, whichever is largest. The rendered image size will depend on the size of the browser window, so this should be set high enough to not cause a deterioration in quality

**GALLERY_RESIZE_QUALITY** -- Default: 80

JPEG quality (0-100) of the preview and thumbnail images

**GALLERY_HDPI_FACTOR** -- Default: 2

The actual preview and thumbnail sizes are multiplied by this number, but rendered according to the quoted value. This enables high dpi displays, such as many mobile devices to show more detail and take advantage of their extra resolution. Some go up to 4x now, so recommended values are 1-4

**GALLERY_IMAGE_MARGIN** -- Default: 6

Margin between thumbnails in px. Some may prefer a less condensed look, so increase this value if your template requires it


Troubleshooting
---------------

**Broken image links after upload**

Check your MEDIA settings. If the media location on disk is changed, you will need to copy the files in the CACHE directory to the new location, or delete and re-upload the broken images

**Errors during upload**

Your server may have a limit on maximum request size (e.g. client_max_body_size for nginx). This needs to be larger than the combined total of all the images your are uploading at once. Also the timeout may need to be extended as preview and thumbnail caches are generated at the time of upload

**Delay when dragging images into upload box**

If you are using Firefox on Linux, there can be a delay before the upload box flashes to acknowledge the pending files, proportional to the number of files. You can use another browser such as Chrome if this is inconvenient.

Credits
-------

Starcross Gallery is by Alex Luton <gallery@starcross.eu>, published under GNU LGPLv3


Album icon by Google licensed CC BY 3.0

Focal Length icon by Ilaria Bernareggi from the Noun Project

Other image data icons made by Freepik www.flaticon.com licensed by CC 3.0 BY