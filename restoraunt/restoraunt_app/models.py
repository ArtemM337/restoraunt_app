from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin_manager", "Admin Manager"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    image = models.ImageField(upload_to="dishes/", blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_METHODS = (
        ("online", "Online payment"),
        ("cash", "Cash on delivery"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=7, decimal_places=2)


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dish.name} - {self.rating}★"
