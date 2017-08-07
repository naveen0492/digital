# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from tags.models import Tag

# Create your models here.
class TagViewManager(models.Manager):
    def count(self,user,tag):
        obj,created = self.model.objects.get_or_create(tag=tag)

        obj.count += 1
        obj.save()
        return obj
class TagView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
    tag = models.ForeignKey(Tag)
    count = models.IntegerField(default=0)

    objects = TagViewManager()

    def __str__(self):
        return str(self.tag.title)
