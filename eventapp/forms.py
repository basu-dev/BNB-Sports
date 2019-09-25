from django import forms
from .models import Postevent, Images, People


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    description = forms.Textarea()

    class Meta:
        model = Postevent
        fields = ("title", "description")


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label="Image")

    class Meta:
        model = Images
        fields = ("image",)


class Personimageform(forms.ModelForm):
    personimage = forms.ImageField()

    class Meta:
        model = People
        fields = ("image",)

