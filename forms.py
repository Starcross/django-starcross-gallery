from django import forms
from PIL import Image


class ImageFileInput(forms.ClearableFileInput):

    def validate(self, value):
        return super.validate(value)


class ImageCreateForm(forms.Form):
    data = forms.FileField(widget=ImageFileInput(attrs={'multiple': True}))

    def clean(self):
        """ Validate files by checking they can be opened by PIL """
        # cleaned_data = super(ImageCreateForm, self).clean()
        image_files = self.files.getlist('data')
        invalid_images = []
        for img in image_files:
            try:
                with Image.open(img) as i:
                    i.verify()
            except (IOError, SyntaxError):
                invalid_images += [img]
        if invalid_images:
            image_names = [i._name for i in invalid_images]
            raise forms.ValidationError("Unable to add invalid images: {0}".format(image_names))
