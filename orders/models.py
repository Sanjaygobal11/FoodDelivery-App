from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    CATEGORY_CHOICES = [
        ('Fast Food', 'Fast Food'),
        ('South Indian', 'South Indian'),
        ('Chinese', 'Chinese'),
        ('Non-Veg', 'Non-Veg'),
        ('Veg', 'Veg'),
        ('Desserts', 'Desserts'),
        ('Drinks', 'Drinks'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.customer_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"
        
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    payment_method = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.customer_name