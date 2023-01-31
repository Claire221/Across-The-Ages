from django import forms
from .models import Contact


class ContactForm(forms.Form):
    class Meta:
        model = Contact

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'message': 'Message',
        }


        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'paragraph-text black-border-light contact-input'
            self.fields[field].label = False