from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from main.models import Ingredient, Product

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CreateIngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'product']

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'breakout']
