from django import forms
from myapp.models import Books
from django.contrib.auth.models import User



class BookForm(forms.Form):

    bookname=forms.CharField()
    authorname=forms.CharField()
    price=forms.IntegerField()
    category=forms.CharField()
    publishdate=forms.DateField()

class BookModelForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={
            "bookname":forms.TextInput(attrs={"class":"form-control"}),
            "authorname":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "category":forms.TextInput(attrs={"class":"form-control"}),
            "publishdate":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

        






