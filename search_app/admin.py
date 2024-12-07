from django.contrib import admin 
from .models import Product, Category, Favorite, CartItem, PurchaseHistory 
 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'auto_restock', 'restock_threshold', 'restock_amount')
    list_filter = ('auto_restock',)
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(CartItem)
admin.site.register(PurchaseHistory) 
