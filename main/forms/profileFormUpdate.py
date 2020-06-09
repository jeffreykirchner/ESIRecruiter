from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from main.models import genders,profile,accountTypes,majors

import logging
import re

class profileFormUpdate(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    chapman_id = forms.CharField(label='Chapman ID', max_length=25,required=False)  
    email = forms.EmailField(label='Email Address (Verification required.)')
    gender =  forms.ModelChoiceField(label="To which gender identity do you most identify?",
                                     queryset=genders.objects.all(),
                                     widget=forms.Select(attrs={"v-model":"profile.gender"}))  
    password1 = forms.CharField(label='Password (Leave blank for no change.)',widget=forms.PasswordInput(),required=False)
    password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput(),required=False)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(profileFormUpdate, self).__init__(*args, **kwargs)

    #check that passwords match
    def clean_password1(self):
        if self.data['password1'] != "":        
            password1 = self.data['password1']

            if password1 != self.data['password2']:
                raise forms.ValidationError('Passwords are not the same')
            
            if validate_password(password1):
                raise forms.ValidationError('Password Error')

            return password1
        else:
            return ""

     #check that username/email not already in use
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exclude(id = self.user.id).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email

