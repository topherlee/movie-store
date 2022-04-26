from django.contrib import admin

from movie_store.models import Artist, Director, Genre, IMDB_rating, Movies, Year_released, Customer

# Register your models here.
class ArtistInline(admin.TabularInline):
    model = Movies.artist.through

class ArtistAdmin(admin.ModelAdmin):
    inlines = [
        ArtistInline,
    ]

class MoviesAdmin(admin.ModelAdmin):
    inlines = [
        ArtistInline,
    ]
    exclude = ('artist',)

#admin.site.register(Artist, ArtistAdmin)
#admin.site.register(Director)
#admin.site.register(Genre)
#admin.site.register(IMDB_rating)
admin.site.register(Movies, MoviesAdmin)
#admin.site.register(Movies)
#admin.site.register(Year_released)
admin.site.register(Customer)

