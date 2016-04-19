# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm


def save_user(form_instance, profile_callback=None):
    """
    Create a new **active** user from form data.

    This method is intended to replace the ``save`` of
    ``django-registration``s ``RegistrationForm``. Calls
    ``profile_callback`` if provided. Required form fields
    are ``username``, ``email`` and ``password1``.
    """
    username = form_instance.cleaned_data['username']
    email = form_instance.cleaned_data['email']
    password = form_instance.cleaned_data['password1']
    new_user = User.objects.create_user(username, email, password)
    new_user.first_name = form_instance.cleaned_data['first_name']
    new_user.last_name = form_instance.cleaned_data['last_name']
    new_user.save()
    if profile_callback is not None:
        profile_callback(user=new_user)
    return new_user


class InvitationForm(forms.Form):
    email = forms.EmailField()


class RegistrationFormInvitation(RegistrationForm):
    """
    Subclass of ``registration.RegistrationForm`` that create an **active**
    user.

    Since registration is (supposedly) done via invitation, no further
    activation is required. For this reason ``email`` field always return
    the value of ``email`` argument given the constructor.
    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(),
                                label= "Логин",
                                error_messages={'invalid': "Это поле может содержать только латинские буквы, цифры и подчеркивание."})
    first_name = forms.CharField(label=u'Имя',required=True,max_length=30)
    last_name = forms.CharField(label=u'Фамилия',required=True,max_length=30)

    def __init__(self, email, *args, **kwargs):
        super(RegistrationFormInvitation, self).__init__(*args, **kwargs)
        self._make_email_immutable(email)

    def _make_email_immutable(self, email):
        self._email = self.initial['email'] = email
        if 'email' in self.data:
            self.data = self.data.copy()
            self.data['email'] = email
        self.fields['email'].widget.attrs.update({'readonly': True})

    def clean_email(self):
        return self._email

    save = save_user
