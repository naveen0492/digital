# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product,MyProducts,Thumbnail
# Register your models here.
class ThumbnailInline(admin.TabularInline):
    model = Thumbnail

class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]

    class Meta:
        model = Product

admin.site.register(Product,ProductAdmin)

admin.site.register(MyProducts)

admin.site.register(Thumbnail)
