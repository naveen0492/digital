# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.conf import settings
from mimetypes import guess_type
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from models import Product
from .forms import ProductModel
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView,UpdateView
from dm.mixins import MultiSlugMixin,SubmitBtnMixin,LoginRequiredMixin
from django.core.urlresolvers import reverse
from wsgiref.util import FileWrapper
from django.db.models import Q
from tags.models import Tag


# Create your views here.
class ProductList(ListView):
    model = Product
    template_name = "list_view.html"

    def get_queryset(self,*args,**kwargs):
        qs = super(ProductList, self).get_queryset(**kwargs)
    	query = self.request.GET.get("q")
        if query:
        	qs = qs.filter(
        			Q(title__icontains=query)|
        			Q(description__icontains=query)
        		).order_by("title")
    	return qs




class ProductDetail(LoginRequiredMixin,MultiSlugMixin,DetailView):
    model = Product
    template_name = "detail_view.html"

    def get_queryset(self,*args,**kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        for tag in tags:
            new_view = TagView.objects.count(self.request.user, tag)
        return context


class ProductDownload(LoginRequiredMixin,MultiSlugMixin,DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
                filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
                guessed_type = guess_type(filepath)[0]
                wrapper = FileWrapper(file(filepath))
                mimetype = 'application/force-download'
                if guessed_type:
                    mimetype = guessed_type
                response = HttpResponse(wrapper, content_type=mimetype)

                if not request.GET.get("preview"):
                    response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)

                response["X-SendFile"] = str(obj.media.name)
                return response
        else:
                raise Http404





class ProductAdd(LoginRequiredMixin,SubmitBtnMixin,CreateView):
    form_class = ProductModel
    template_name = "form.html"
    submit_btn = "Add"


    def form_valid(self,form):
        user = self.request.user
        form.instance.user = user

        valid_data = super(ProductAdd,self).form_valid(form)
        form.instance.managers.add(user)
        tags = form.cleaned_data.get("tags")
        if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(form.instance)
        return valid_data

class ProductUpdate(LoginRequiredMixin,SubmitBtnMixin,MultiSlugMixin,UpdateView):
    model = Product
    form_class = ProductModel
    template_name = "form.html"
    submit_btn = "Update"


    def get_initial(self):
    		initial = super(ProductUpdate,self).get_initial()
    		print initial
    		tags = self.get_object().tag_set.all()
    		initial["tags"] = ", ".join([x.title for x in tags])
    		"""
    		tag_list = []
    		for x in tags:
    			tag_list.append(x.title)
    		"""
    		return initial

    """def get_success_url(self):
        return reverse("products:detail")"""

    def get_object(self,*args,**kwargs):
        user = self.request.user
        obj = super(ProductUpdate,self).get_object(*args,**kwargs)
        if obj.user == user or obj.user in managers:
            return obj
        else :
            raise Http404

    def form_valid(self, form):
		valid_data = super(ProductUpdate, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(",")

			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(self.get_object())
		return valid_data


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
