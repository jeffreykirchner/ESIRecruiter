from django import forms

import logging

#form
class loginForm(forms.Form):

    username =  forms.EmailField(label='Email address (lower case)')

    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs={"type":"password"}))               
