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

1. Add "gallery" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gallery',
    ]

2. Include the gallery URLconf in your project urls.py like this with your preferred location e.g. "gallery/"::

    path('gallery/', include('gallery.urls')),

3. Run `python manage.py migrate gallery` to create the models.

4. Start the development server and create any albums you required in http://127.0.0.1:8000/admin/. It's not necessary to create albums if you prefer just a single image feed

5. Visit http://127.0.0.1:8000/gallery/ to access your image feed. Drag your images onto the page and you will see a flashing highlighted box.


Credits
-------

Starcross Gallery is by Alex Luton <info@starcross.eu>, published under GNU LGPLv3

Album icon by Google licensed CC BY 3.0