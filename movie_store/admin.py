from django.contrib import admin

from movie_store.models import Actor, Director, Genre, Movie, Customer, Comment

# Register your models here.
class ArtistInline(admin.TabularInline):
    model = Movie.actor.through

class ArtistAdmin(admin.ModelAdmin):
    inlines = [
        ArtistInline,
    ]

class MoviesAdmin(admin.ModelAdmin):
    inlines = [
        ArtistInline,
    ]
    exclude = ('actor',)

#admin.site.register(Artist, ArtistAdmin)
#admin.site.register(Director)
#admin.site.register(Genre)
admin.site.register(Movie, MoviesAdmin)
#admin.site.register(Movies)
admin.site.register(Customer)
admin.site.register(Comment)

