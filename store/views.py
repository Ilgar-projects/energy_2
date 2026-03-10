from django.shortcuts import render

from .models import Product


def home(request):
    products = Product.objects.filter(is_active=True)
    hero = products.filter(hero_product=True).first() or products.first()
    return render(request, "store/home.html", {"hero": hero})


def catalog(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/catalog.html", {"products": products})
