from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'
    verbose_name = 'Starcross Gallery'

    def ready(self):
        import gallery.signals
