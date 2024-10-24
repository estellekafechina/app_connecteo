from django import forms
from django.contrib.auth.models import User
from .models import Profile, Message
from django.contrib.auth.forms import UserChangeForm ,UserCreationForm
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
    


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Entrez votre prénom.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Entrez votre nom.")
    email = forms.EmailField(max_length=254, required=True, help_text="Entrez une adresse e-mail valide.")
    age = forms.IntegerField(required=True, help_text="Entrez votre âge.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2']


