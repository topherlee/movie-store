from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Director

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    address = forms.CharField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1','password2','email','address')#,"first_name","last_name","email","password")

class MoviesForm (forms.ModelForm):
    #title = forms.CharField(label='Title',max_length=500)
    
    class Meta:
        model = Movie
        fields = "__all__"#('title','price','year_released','imdb_rating','director')
