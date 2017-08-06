# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage

# Create your models here.
def download_location(instance,filename):
    return "%s/%s" %(instance.slug,filename)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    media = models.FileField(null=True,
                            blank=True,
                            upload_to=download_location ,
                            storage=FileSystemStorage(
                            location=settings.PROTECTED_ROOT),
                            )
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='product_manager')
    title = models.CharField(max_length=30)
    slug = models.SlugField(blank=True,unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:detail",kwargs={"slug":self.slug})

    def get_download(self):
        return reverse("products:download",kwargs={"slug":self.slug})

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)


class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return "%s" %(self.products.count())

def Thumbnail_location(instance,filename):
    return "%s/%s" %(instance.product.slug,filename)

class Thumbnail(models.Model):

    product = models.ForeignKey(Product)
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(null=True,
                            blank=True,
                            upload_to=Thumbnail_location ,
                            height_field="height",
                            width_field="width",
                            )
    def __str__(self): # __str__(self):
		return str(self.media.path)

import os
from PIL import Image
import random
from django.core.files import File

def thumbnail_post_save_reciever(sender, instance, *args, **kwargs):
    if instance.media:
        hd,hd_created = Thumbnail.objects.get_or_create(product=instance)
        hd_size=(300,300)

        if hd_created:

            filename = os.path.basename(instance.media.path)
            thumb = Image.open(instance.media.path)
            thumb.thumbnail(hd_size,Image.ANTIALIAS)

            temp_loc = "%s/%s/temp" %(settings.MEDIA_ROOT,instance.slug)
            if not os.path.exists(temp_loc):
                os.makedirs(temp_loc)
            temp_file_path = os.path.join(temp_loc,filename)

            if os.path.exists(temp_file_path):
                temp_path = os.path.join(temp_loc,"%s" %random.random())
                os.makedirs(temp_path)
                temp_file_path = os.path.join(temp_path,filename)
            temp_image = open(temp_file_path,"w")
            thumb.save(temp_image)
            thumb_data = open(temp_file_path,"r")
            thumb_file = File(thumb_data)
            hd.media.save(filename,thumb_file)








post_save.connect(thumbnail_post_save_reciever, sender=Product)
