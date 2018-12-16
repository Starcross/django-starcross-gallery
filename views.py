from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from gallery.models import Image, Album
from gallery.forms import ImageCreateForm
from gallery import settings


class ImageView(DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['album_images'] = []
        context['apk'] = self.kwargs.get('apk')

        # If there is an album in the context, look up the images in it
        if context['apk']:
            context['album'] = Album.objects.get(pk=context['apk'])
            context['album_images'] = context['album'].images.all
        return context


class ImageList(ListView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageList, self).get_context_data(**kwargs)
        context['image_margin'] = settings.IMAGE_MARGIN
        return context


class ImageCreate(LoginRequiredMixin, FormView):
    """ Embedded drag and drop image upload"""
    login_url = '/admin/login/'
    form_class = ImageCreateForm
    template_name = 'gallery/image_upload.html'

    def form_valid(self, form):
        """ Bulk create images based on form data """
        image_data = form.files.getlist('data')
        for data in image_data:
            image = Image.objects.create(data=data)
            image.image_albums.set(form.data['apk'])
        messages.success(self.request, "Images added successfully")
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return_url = reverse('gallery:image_list')
        if next_url:
            return_url = next_url
        return return_url

    def form_invalid(self, form):
        response = super().form_invalid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            # TODO: Preserve error message
            return redirect(next_url)
        else:
            return response


class AlbumView(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        return context


class AlbumList(ListView):
    model = Album
    template_name = 'gallery/album_list.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumList, self).get_context_data(**kwargs)
        context['image_margin'] = settings.IMAGE_MARGIN
        return context

    def get_queryset(self):
        # Return a list of albums containing a highlight even if none is selected
        album_list = []
        for album in super(AlbumList, self).get_queryset():
            # if there is no highlight but there are images in the album, use the first
            if not album.highlight and album.images.count():
                first_image = album.images.earliest('id')
                album.highlight = first_image
            album_list.append(album)
            if album.highlight:
                album.highlight.title = album.title  # override highlight title
        return album_list
