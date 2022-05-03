from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Director(models.Model):
    name = models.CharField(unique=True, max_length=200)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

class Movie(models.Model):
    title = models.CharField(max_length=1000)   
    year_released = models.IntegerField(validators=[MaxValueValidator(2030),MinValueValidator(1800)])
    imdb_rating = models.DecimalField(decimal_places=1, max_digits=3, null=True, blank=True)
    imdb_votes = models.CharField(max_length=100, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actor = models.CharField(max_length=1000, blank=True)
    genre = models.CharField(max_length=500, blank=True)
    metascore = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100),MinValueValidator(0)])
    runtime = models.IntegerField(blank=True, null=True)
    rating = models.CharField(blank=True, null=True, max_length=50)
    plot_summary = models.TextField(blank=True)
    tagline = models.TextField(blank=True)
    poster_link = models.URLField()
    imdb_link = models.URLField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title},{self.price}'

class Cart(models.Model):
    product = models.ForeignKey(Movie, on_delete=models.CASCADE)
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
    product = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product},{self.cart},{self.order},{self.created_date}'

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User,editable=False,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return '{} by {}'.format(self.body, self.user)