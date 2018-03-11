from django.views.generic import DetailView, ListView

from gallery.models import Image, Album
from gallery import settings


class ImageView(DetailView):
    model = Image
    
    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['album_images'] = []
        context['apk'] = self.kwargs.get('apk')
        context['album'] = Album.objects.get(pk=context['apk'])
        # If there is an album in the context, look up the images in it
        if context['album']:
            context['album_images'] = context['album'].images.all
        return context


class ImageList(ListView):
    model = Image


class AlbumView(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        return context


class AlbumList(ListView):
    model = Album
    template_name = 'gallery/album_list.html'

    def get_queryset(self):
        # Return a list of albums containing a highlight even if none is selected
        album_list=[]
        for album in super(AlbumList, self).get_queryset():
            # if there is no highlight but there are images in the album, use the first
            if not album.highlight and album.images.count():
                first_image = album.images.earliest('id')
                album.highlight = first_image
            album_list.append(album)
            if album.highlight:
                album.highlight.title = album.title # override highlight title
        return album_list

