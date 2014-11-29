from django.conf.urls import patterns, url

from gallery.views import ImageView, ImageList, AlbumView, AlbumList

urlpatterns = patterns('',
    # ex: /gallery/
    #url(r'^$', ImageList.as_view()),
    # ex: /gallery/5/
    url(r'^$', AlbumList.as_view()),
    url(r'^image/$', ImageList.as_view(), name='image_list'),
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image_detail'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album_detail'),
    url(r'^album/(?P<apk>\d+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='album_image_detail'),

)