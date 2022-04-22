from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

    def __str__(self):
        return str(self.title)
