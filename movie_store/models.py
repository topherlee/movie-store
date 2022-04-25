from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Year_released(models.Model):
    year = models.IntegerField(unique=True, validators=[MaxValueValidator(2022),MinValueValidator(1800)])

    def __str__(self):
        return str(self.year)

class IMDB_rating(models.Model):
    rating = models.DecimalField(unique=True, decimal_places=1, max_digits=3)

    def __str__(self):
        return str(self.rating)

class Director(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return str(self.name)

class Artist(models.Model):
    name = models.CharField(unique=True, max_length=200)
    
    def __str__(self):
        return str(self.name)

class Genre(models.Model):
    genre = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return str(self.genre)

class Movies(models.Model):
    year_released = models.ForeignKey(Year_released, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    imdb_rating = models.ForeignKey(IMDB_rating, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
    genre = models.ManyToManyField(Genre)
    runtime = models.IntegerField()
    certificate = models.CharField(null=True, max_length=50)
    plot_summary = models.TextField()
    poster_link = models.URLField()
    gross = models.CharField(null=True, max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title},{self.price}'

class Cart(models.Model):
    product = models.ForeignKey(Movies, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product},{self.quantity},{self.created_date}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    address = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}, {self.address}'

    class Meta:
        db_table = 'customer'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'

class LineItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Movies, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product},{self.cart},{self.order},{self.created_date}'
