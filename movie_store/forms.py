from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Comment, Customer

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    address = forms.CharField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1','password2','email','address')

class MoviesForm (forms.ModelForm):
    
    class Meta:
        model = Movie
        fields = "__all__"

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class BasketAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int,
    )
    override = forms.BooleanField(
        required=False,initial=False,widget=forms.HiddenInput
    )
    
    def __init__(self, *args, **kwargs):
        super(BasketAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = "Qty:"

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ("address",)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name","last_name","email",)
