import logging

from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

logger = logging.getLogger('cookbook.custom')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'recipes_search.html')

    return render(request, 'info.html')


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password = forms.CharField(
        label="Password", max_length=128
    )
    password_confirm = forms.CharField(
        label="Password confirmation", max_length=128
    )

    class Meta:
        model = User
        fields = ("username", 'email')
        field_classes = {'username': UsernameField, 'email': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password_confirm'), self.instance)
        return password_confirm

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    else:
        form = UserCreationForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'register.html', args)
