from django.db import models
from django.contrib.auth.models import User

class Category(models.Model): 
    name = models.CharField(max_length=255) 
 
    def __str__(self): 
        return self.name 
 
class Product(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # 1はカテゴリID
    stock = models.PositiveIntegerField(default=0)  # 在庫
    sales_count = models.PositiveIntegerField(default=0)  # 販売数
 
    def __str__(self): 
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    @classmethod
    def is_favorite(cls, user, product):
        return cls.objects.filter(user=user, product=product).exists()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}が{self.product.name}を{self.quantity}個購入"
