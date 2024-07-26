from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
import secrets

from .paystack import PayStack

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Categories"

    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

# 
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/')

#     def __str__(self):
#         return f"Image for {self.product.name}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('NOT DELIVERED', 'Not Delivered'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='NOT DELIVERED')
    delivered = models.BooleanField(default=False)
    total_price = models.IntegerField()
    received = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=15, default="coins")
    
    

class OrderItem(models.Model):
    price = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Escrow(models.Model):
    buyer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='buyer_escrows')
    vendor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='vendor_escrows')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    price = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_purchased = models.BooleanField(default=False)
   
class Bargain(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    approved = models.BooleanField(default=False)

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            print(f"res_amount: {result['amount']} self_amount: {self.amount}")
            if result["amount"]  == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
            

    def __str__(self):
        return self.amount

    
