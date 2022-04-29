from django.contrib import admin

from movie_store.models import Artist, Director, Genre, Movies, Customer

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
admin.site.register(Movies, MoviesAdmin)
#admin.site.register(Movies)
admin.site.register(Customer)

