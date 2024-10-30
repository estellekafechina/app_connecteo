from django import forms
from django.contrib.auth.models import User
from .models import Profile, Message
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

#formulaire de création de message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

# Formulaire de mise à jour des informations de l'utilisateur
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

# Formulaire de mise à jour du profil utilisateur
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            if profile_image.size > 5 * 1024 * 1024: 
                raise ValidationError("La taille de l'image ne doit pas dépasser 5MB.")
        return profile_image

# Formulaire de création d'un nouvel utilisateur personnalisé
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Entrez votre prénom.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Entrez votre nom.")
    email = forms.EmailField(max_length=254, required=True, help_text="Entrez une adresse e-mail valide.")
    age = forms.IntegerField(required=True, help_text="Entrez votre âge.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 13:
            raise ValidationError("Vous devez avoir au moins 13 ans pour vous inscrire.")
        return age

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return password2