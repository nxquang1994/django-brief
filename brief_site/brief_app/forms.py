from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_empty(value):
    if value is None:
        raise ValidationError(
            _('%(value)s cannot be empty'),
            params={'value': value}
        )

def validate_wrong_title(value):
    if value == 'KKK':
                raise ValidationError(
            _('%(value)s cannot be KKK'),
            params={'value': value}
        )

def validate_wrong_title1(value):
    if value == 'KKK':
                raise ValidationError(
            _('%(value)s cannot be KKK JJJ'),
            params={'value': value}
        )

class RssFeedItemForm(forms.Form):
    title = forms.CharField(label='Title', validators=[validate_empty, validate_wrong_title],  widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.CharField(label='Category', validators=[validate_empty, validate_wrong_title, validate_wrong_title1],  widget=forms.TextInput(attrs={'class': "form-control"}))
    link = forms.CharField(label='Link', validators=[validate_empty],  widget=forms.TextInput(attrs={'class': "form-control"}))
    published_date = forms.DateField(label='Published date', validators=[validate_empty],  widget=forms.TextInput(attrs={'class': "form-control date-picker"}))
    pass