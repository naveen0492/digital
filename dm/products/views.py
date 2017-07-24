# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from models import Product
from .forms import ProductModel
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView,UpdateView
from dm.mixins import MultiSlugMixin,SubmitBtnMixin


# Create your views here.
class ProductList(ListView):
    model = Product
    template_name = "list_view.html"

    def get(self,*args,**kwargs):
        product = super(ProductList,self).get(*args,**kwargs)
        return product
    def get_context_data(self,**kwargs):
        context = super(ProductList,self).get_context_data(**kwargs)
        context['product'] = Product.objects.all()
        return context


class ProductDetail(MultiSlugMixin,DetailView):
    model = Product
    template_name = "detail_view.html"
    def get_queryset(self,*args,**kwargs):
        qs = super(ProductDetail,self).get_queryset(*args,**kwargs)
        return qs

class ProductAdd(SubmitBtnMixin,CreateView):
    form_class = ProductModel
    template_name = "form.html"
    submit_btn = "Add"
    success_url = "create"

class ProductUpdate(SubmitBtnMixin,MultiSlugMixin,UpdateView):
    model = Product
    form_class = ProductModel
    template_name = "form.html"
    submit_btn = "Update"
    success_url = "create"



def update_view(request,object_id=None):
    product = get_object_or_404(Product,id=object_id)
    form = ProductModel(request.POST or None,instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()

    template = "update.html"
    context = {
    "form": form,
    }
    return render(request, template, context)


def create_product(request):
    form = ProductModel(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()

    template = "create.html"
    context = {
    "form": form,
    }
    return render(request, template, context)

def list_view(request):
    product = Product.objects.all()
    context = {
    "product": product
    }
    template = "list_view.html"
    return render(request,template,context)

def detail_view(request,object_id=None):
    product = Product.objects.get(id=object_id)
    context = {
        "product":product
    }
    template = "detail_view.html"
    return render(request,template,context)
def detail_slug_view(request,slug=None):
    product = Product.objects.get(slug=slug)
    context = {
        "product":product
    }
    template = "detail_view.html"
    return render(request,template,context)
