"""
Definition of forms.
"""

from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User, Report

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

class LoginForm(forms.ModelForm):
    use_required_attribute = False
    def onlyInt(val):
        if not val.isdigit():
            raise ValidationError('ID contains characters')

    class Meta:
        model = User
        fields = ['ic_num', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['ic_num'].widget = forms.NumberInput()
        self.fields['ic_num'].widget.attrs['class'] = 'form-control'
        #self.fields['ic_num']
        self.fields['ic_num'].widget.attrs['placeholder'] = 'IC Number'
        self.fields['ic_num'].label = 'IC Number'
        self.fields['ic_num'].help_text = ''

        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].label = 'Password'
        self.fields['password'].type = 'password'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].help_text = ''

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email Address"}))
    # first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name"}))
    # last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name"}))
    use_required_attribute = False
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
        fields = ['first_name', 'last_name', 'ic_num', 'phone_num', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].help_text = ''

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].help_text = ''
        
        self.fields['ic_num'].widget.attrs['class'] = 'form-control'
        self.fields['ic_num'].widget.attrs['placeholder'] = 'IC Number'
        self.fields['ic_num'].label = 'IC Number'
        self.fields['ic_num'].help_text = ''
        #self.fields['ic_num'].validators = [onlyInt, MaxLengthValidator(12)]
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = 'Email Address'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].help_text = ''
        
        self.fields['phone_num'].widget.attrs['class'] = 'form-control'
        self.fields['phone_num'].label = 'Phone Number'
        self.fields['phone_num'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phone_num'].help_text = ''
        #self.fields['phone'].validators = [phoneValidator]
        

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = '<ul class="form-text text-muted" small><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</span>'

        self.fields['role'].widget.attrs['style'] = 'display: none;'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ReportForm(forms.ModelForm):
    use_required_attribute = False

    photo = MultipleFileField(label='Select files', required=False)
    photo.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Report
        fields = ['title', 'description', 'category', 'photo']
    
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget = forms.TextInput()
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].label = 'Title'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['title'].help_text = ''
    

        """
        self.fields['imgs'].widget = forms.ImageField()
        self.fields['imgs'].widget.attrs['class'] = 'form-control'
        self.fields['imgs'].label = 'Images'
        self.fields['imgs'].widget.attrs['placeholder'] = 'Images'
        self.fields['imgs'].help_text = ''
        """
    """
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=500, required=False)
    category = forms.ChoiceField(choices=Report.CATEGORY.choices, required=True)
    loc_lng = forms.DecimalField(required=True)
    loc_lat = forms.DecimalField(required=True)
    
    """