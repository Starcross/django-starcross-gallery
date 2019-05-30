from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from gallery.models import Image, Album
from gallery.forms import ImageCreateForm
from gallery import settings


class GallerySettingsMixin(object):
    """ Apply Gallery's Settings to a view """

    def get_context_data(self, **kwargs):
        """ Make settings available the template """
        context = super(GallerySettingsMixin, self).get_context_data(**kwargs)
        context['logo_path'] = settings.GALLERY_LOGO_PATH
        context['gallery_title'] = settings.GALLERY_TITLE
        context['hdpi_factor'] = settings.GALLERY_HDPI_FACTOR
        context['image_margin'] = settings.GALLERY_IMAGE_MARGIN
        context['footer_info'] = settings.GALLERY_FOOTER_INFO
        context['footer_email'] = settings.GALLERY_FOOTER_EMAIL

        return context


class ImageView(GallerySettingsMixin, DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['album_images'] = []
        context['apk'] = self.kwargs.get('apk')

        context['next_image'] = None
        context['previous_image'] = None

        # If there is an album in the context, look up the images in it
        if context['apk']:
            context['album'] = Album.objects.get(pk=context['apk'])
            images = context['album'].images.all()
            album_images = sorted(images, key=lambda i: i.date_taken)
            context['album_images'] = album_images
            for i in range(len(album_images)):
                if self.object.pk == album_images[i].pk:
                    if i > 0:
                        context['previous_image'] = album_images[i - 1]
                    if i < len(album_images) - 1:
                        context['next_image'] = album_images[i + 1]
        else:
            # Look for albums this image appears in
            context['albums'] = self.object.image_albums.all()

        return context


class ImageList(GallerySettingsMixin, ListView):
    model = Image

    def get_queryset(self):
        # Order by newest first
        return super(ImageList, self).get_queryset().order_by('-pk')


class ImageCreate(GallerySettingsMixin, LoginRequiredMixin, FormView):
    """ Embedded drag and drop image upload"""
    login_url = '/admin/login/'
    form_class = ImageCreateForm
    template_name = 'gallery/image_upload.html'

    def form_valid(self, form):
        """ Bulk create images based on form data """
        image_data = form.files.getlist('data')
        for data in image_data:
            image = Image.objects.create(data=data)
            image.image_albums.add(form.data['apk'])
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


class AlbumView(GallerySettingsMixin, DetailView):
    model = Album

    def get_queryset(self):
        album = super(AlbumView, self).get_queryset()
        return album

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        images = context['album'].images.all()
        context['images'] = sorted(images, key=lambda i: i.date_taken)
        return context


class AlbumList(GallerySettingsMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'


