from celery import shared_task
from .models import Product
from django.db import models

@shared_task
def auto_restock_products():
    products = Product.objects.filter(auto_restock=True, stock__lt=models.F('restock_threshold'))
    for product in products:
        product.stock += product.restock_amount
        product.save()