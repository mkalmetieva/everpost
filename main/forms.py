from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User

from main.models import Post, NicEditImage
from main.utils import sanitize_html
from main.widgets import NicEditWidget


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'text': NicEditWidget(attrs={'style': 'width: 800px;'}),
        }
        fields = ('title', 'text')

    def clean_text(self):
        text = self.cleaned_data.get("text")
        sanitized_text = sanitize_html(text)
        return sanitized_text


class NicEditImageForm(forms.ModelForm):
    class Meta:
        model = NicEditImage
        fields = '__all__'
