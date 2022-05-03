from django.contrib import admin

from movie_store.models import Movie, Customer, Comment

# Register your models here.
#admin.site.register(Artist, ArtistAdmin)
#admin.site.register(Director)
#admin.site.register(Genre)
admin.site.register(Movie)
#admin.site.register(Movies)
admin.site.register(Customer)
admin.site.register(Comment)

