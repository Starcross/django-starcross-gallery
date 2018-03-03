from django.urls import path

from gallery.views import ImageView, ImageList, AlbumView, AlbumList

app_name = 'gallery'
urlpatterns = [
    # ex: /gallery/
    #path('', ImageList.as_view()),
    # ex: /gallery/5/
    path('', AlbumList.as_view(), name='album_list'),
    path('image/', ImageList.as_view(), name='image_list'),
    path('image/<int:pk>/<slug>', ImageView.as_view(), name='image_detail'),
    path('album/<int:pk>/<slug>/', AlbumView.as_view(), name='album_detail'),
    path('album/<int:apk>/<int:pk>/<slug>', ImageView.as_view(), name='album_image_detail')
]
