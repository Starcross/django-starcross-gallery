import PIL
from django import forms
from PIL import Image


# Referring to https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#uploading-multiple-files

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

    def validate(self, value):
        """ Validate file by checking it can be opened by PIL """
        try:
            Image.open(value)
        except PIL.UnidentifiedImageError as e:
            raise forms.ValidationError("Unable to add invalid image: {0}".format(value.name))


class ImageCreateForm(forms.Form):
    data = MultipleFileField()
