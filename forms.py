from django import forms


class ImageFileInput(forms.ClearableFileInput):

    def validate(self, value):
        return super.validate(value)


class ImageCreateForm(forms.Form):
    data = forms.FileField(widget=ImageFileInput(attrs={'multiple': True}))

