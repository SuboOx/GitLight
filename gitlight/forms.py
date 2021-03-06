from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mdeditor.fields import MDTextFormField

from gitlight.models import Profile

MAX_UPLOAD_SIZE = 2500000


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "Username"}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "Password"}))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "Username"}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "First Name"}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "Last Name"}))
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control form-control-user', 'placeholder': "Email"}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control form-control-user', 'placeholder': "Password"}))
    confirm_password = forms.CharField(max_length=200,
                                       label='Confirm password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                         'placeholder': "Confirm Password"}))

    def clean_confirm_password(self):
        """Handle password mismatch."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        """Handle mulitiple usernames"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class CreateRepoForm(forms.Form):
    repo_name = forms.CharField(max_length=200)
    # TODO: except handler, What if have same name


class IssueForm(forms.Form):
    issue_title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': "Title"}))
    content = MDTextFormField()


class ReplyForm(forms.Form):
    content = MDTextFormField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio_input_text',)

    def clean_picture(self):
        picture = self.cleaned_data['profile_picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture
