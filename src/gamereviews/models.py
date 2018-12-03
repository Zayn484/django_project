from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from PIL import Image

from .utils import unique_slug_generator


NewsUser = settings.AUTH_USER_MODEL
ReviewUser = settings.AUTH_USER_MODEL
TopgamesUser = settings.AUTH_USER_MODEL

# Create your models here.

class News(models.Model):
    owner       = models.ForeignKey(NewsUser)
    title       = models.CharField(max_length=120)
    category    = models.CharField(max_length=12, null=True, blank=True)
    imgs        = models.FileField()
    info        = models.CharField(max_length=512, null=True, blank=True)
    content     = models.TextField(null=True,blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

class Reviews(models.Model):
    owner       = models.ForeignKey(ReviewUser)
    title       = models.CharField(max_length=120)
    imgs        = models.FileField(null=True, blank=True)
    gameplay    = models.FileField(null=True, blank=True)
    info        = models.CharField(max_length=512, null=True, blank=True)
    content     = models.TextField(null=True, blank=True)
    category    = models.CharField(max_length=20)
    cpu         = models.CharField(max_length=200)
    gpu         = models.CharField(max_length=200)
    ram         = models.CharField(max_length=100)
    space       = models.CharField(max_length=100)
    os          = models.CharField(max_length=200)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

class Topgames(models.Model):
    owner        = models.ForeignKey(TopgamesUser)
    title        = models.CharField(max_length=120)
    imgs         = models.FileField()
    release_date = models.CharField(max_length=50)
    content      = models.CharField(max_length=512)
    timestamp    = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)
    slug         = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title


class Slideshow(models.Model):
    owner        = models.ForeignKey(TopgamesUser)
    imgs         = models.FileField()
    timestamp    = models.DateTimeField(auto_now_add=True)


def pre_save_reciever(sender, instance, *args, **kwargs):
    print('saving')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(pre_save_reciever, sender=News)
pre_save.connect(pre_save_reciever, sender=Reviews)
pre_save.connect(pre_save_reciever, sender=Topgames)