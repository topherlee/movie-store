from django import forms
from .models import IMDB_rating, Movies, Year_released

class MoviesForm (forms.ModelForm):
    #title = forms.CharField(label='Title',max_length=500)
    new_director = forms.CharField(label='New Director Name', required=False, max_length=100)
    
    class Meta:
        model = Movies
        fields = "__all__"#('title','price','year_released','imdb_rating','director')