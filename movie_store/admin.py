from django.contrib import admin

from movie_store.models import Artist, Director, Genre, IMDB_rating, Movies, Year_released

# Register your models here.
admin.site.register(Year_released)
admin.site.register(IMDB_rating)
admin.site.register(Director)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Movies)

