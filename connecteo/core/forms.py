from django import forms
from django.contrib.auth.models import User
from .models import Profile, Message
from django.contrib.auth.forms import UserChangeForm
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'social_links']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
    
class EditProfileForm(UserChangeForm):
    password = None  # On ne veut pas que l'utilisateur modifie le mot de passe via ce formulaire

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']