from django import forms
from .models import Postevent, Images, People
from .widgets import BootstrapDateTimePickerInput


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    description = forms.Textarea()
    event_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"], widget=BootstrapDateTimePickerInput()
    )

    class Meta:
        model = Postevent
        fields = ("title", "event_date", "description")


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

