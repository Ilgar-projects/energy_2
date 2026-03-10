from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, "store/home.html")


def catalog(request):
    products = Product.objects.filter(is_active=True).order_by("sort_order", "id")
    return render(request, "store/catalog.html", {"products": products})