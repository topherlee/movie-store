from django import forms
from .models import IMDB_rating, Movies, Year_released, Director

class MoviesForm (forms.ModelForm):
    #title = forms.CharField(label='Title',max_length=500)
    
    class Meta:
        model = Movies
        fields = "__all__"#('title','price','year_released','imdb_rating','director')
