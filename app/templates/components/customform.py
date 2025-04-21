from django import forms

class ReportForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label='Title',
        
    )