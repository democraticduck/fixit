"""
Definition of forms.
"""

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

class LoginForm(forms.Form):
    """Authentication form which uses boostrap CSS."""
    ic = forms.CharField(max_length=12,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'IC number'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email Address"}))
    # first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name"}))
    # last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name"}))

    def onlyInt(val):
        if not val.isdigit():
            raise ValidationError('ID contains characters')

    def phoneValidator(val):
        if not val.isdigit():
            raise ValidationError('Phone number contains characters')
        if len(val) != 10 or len(val) != 11:
            raise ValidationError('Phone number must be 10 digits')
        

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].label = ''
        self.fields['first_name'].help_text = ''

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].label = ''
        self.fields['last_name'].help_text = ''
        '''
        self.fields['ic_num'].widget.attrs['class'] = 'form-control'
        self.fields['ic_num'].widget.attrs['placeholder'] = 'IC Number'
        self.fields['ic_num'].label = ''
        self.fields['ic_num'].help_text = 'Enter your ic number'
        #self.fields['ic_num'].validators = [onlyInt, MaxLengthValidator(12)]
        '''
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].help_text = ''
        '''
        self.fields['phone_num'].widget.attrs['class'] = 'form-control'
        self.fields['phone_num'].label = ''
        self.fields['phone_num'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phone_num'].help_text = ''
        #self.fields['phone'].validators = [phoneValidator]
        '''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = '<ul class="form-text text-muted" small><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</span>'