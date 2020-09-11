from django import forms
from common_app.models import RssFeedItem

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
        )
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
        )
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
        )
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
        )
    )

    class Meta:
        model = RssFeedItem
        fields = ('category', 'title', 'link', 'published_date')
