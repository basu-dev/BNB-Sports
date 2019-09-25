from django.db import models
from PIL import Image
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.defaultfilters import truncatechars
from .images import make_thumbnail
from django.contrib.auth.models import User


class Postevent(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True, default="aewrf")
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def get_image_filename(instance, filename):
        title = instance.post.title
        slug = slugify(title)
        return "post_images/%s-%s" % (filename)

    @property
    def short_description(self):
        return truncatechars(self.description, 100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return self.title


class Images(models.Model):
    post = models.ForeignKey(Postevent, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to="images/", verbose_name="Image")
    thumbnail = models.ImageField(
        upload_to="thumbnail/",
        verbose_name="thumbnail",
        editable=False,
        default="media/images/150-1.png",
    )

    def save(self, *args, **kwargs):
        # save for image
        super().save(*args, **kwargs)

        make_thumbnail(self.thumbnail, self.image, (200, 200), "thumb")

        # save for thumbnail and icon
        super().save(*args, **kwargs)


class People(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    contact_no = models.IntegerField(10, blank=True, null=True)
    image = models.ImageField(upload_to="people/", null=True, blank=True)


class Members(models.Model):
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    event = models.ForeignKey(Postevent, on_delete=models.CASCADE)

