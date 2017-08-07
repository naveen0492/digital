# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.

from products.models import Product

class TagQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class TagManager(models.Manager):
	def get_queryset(self):
		return TagQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return super(TagManager, self).all(*args, **kwargs).active()


class Tag(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	products = models.ManyToManyField(Product, blank=True)
	active = models.BooleanField(default=True)

	objects = TagManager()

	def __unicode__(self):
		return str(self.title)

	def get_absolute_url(self):
		view_name = "tags:detail"
		return reverse(view_name, kwargs={"slug": self.slug})


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


def tag_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(tag_pre_save_reciever, sender=Tag)
