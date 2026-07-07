from django.contrib.sitemaps.views import sitemap
from django.urls import path

from gallery.sitemaps import ImageSitemap
from gallery.views import ImageView, ImageList, AlbumView, AlbumList, ImageCreate

app_name = 'gallery'

urlpatterns = [
    path('', AlbumList.as_view(), name='album_list'),
    path('images/', ImageList.as_view(), name='image_list'),
    path('image/<int:pk>/<slug>', ImageView.as_view(), name='image_detail'),
    path('upload/', ImageCreate.as_view(), name='image_upload'),
    path('album/<int:pk>/<slug>/', AlbumView.as_view(), name='album_detail'),
    path('album/<int:apk>/<int:pk>/<slug>', ImageView.as_view(), name='album_image_detail'),
    path('sitemap.xml', sitemap, {
            'sitemaps':  {'image': ImageSitemap},
            'template_name': 'gallery/sitemap.xml',
        },
        name='django.contrib.sitemaps.views.sitemap'),
]
