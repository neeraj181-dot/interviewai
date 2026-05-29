from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control glass-input',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control glass-input',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control glass-input',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control glass-input',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control glass-input',
            'placeholder': 'Password'
        })


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control glass-input'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control glass-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control glass-input'})
    )

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'resume', 'skills', 'experience_years', 'github_url', 'linkedin_url', 'theme_accent')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'resume': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'skills': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Python, Django, React, SQL...'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control glass-input', 'min': 0, 'max': 50}),
            'github_url': forms.URLInput(attrs={'class': 'form-control glass-input', 'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control glass-input', 'placeholder': 'https://linkedin.com/in/username'}),
            'theme_accent': forms.HiddenInput(),
        }
