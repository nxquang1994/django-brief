from django import forms
from common_app.models import RssFeedItem
from brief_app.common.define import *

class ItemForm(forms.ModelForm):
    category = forms.CharField(
        label='Category',
        help_text='(Max 50 characters)',
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'true'
            }
        ),
        error_messages = {
            'required': ERROR_MESSAGE_REQUIRED.format('Category'),
            'max_length': ERROR_MESSAGE_MAX.format('Category', 50)
        }
    )
    title = forms.CharField(
        label='Title',
        help_text='(Max 255 characters)',
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages = {
            'required': ERROR_MESSAGE_REQUIRED.format('Title'),
            'max_length': ERROR_MESSAGE_MAX.format('Title', 255)
        }
    )
    link = forms.URLField(
        label='Link',
        help_text='(Max 255 characters)',
        required=True,
        max_length=255,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages = {
            'required': ERROR_MESSAGE_REQUIRED.format('Link'),
            'max_length': ERROR_MESSAGE_MAX.format('Link', 255),
            'invalid': ERROR_MESSAGE_FORMAT.format('link')
        }
    )
    published_date = forms.DateTimeField(
        label='Published Date',
        help_text='(YYYY-MM-DD HH:mm:ss)',
        required=True,
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control date-picker'
            }
        ),
        error_messages = {
            'required': ERROR_MESSAGE_REQUIRED.format('Published date'),
            'invalid': ERROR_MESSAGE_FORMAT.format('published date')
        }
    )

    class Meta:
        model = RssFeedItem
        fields = ('category', 'title', 'link', 'published_date')
