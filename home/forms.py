from django import forms
from .models import Contact, Newsletter


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'message')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'message': 'Message',
        }

        for field in self.fields:
            if field == 'last_name':
                placeholder = placeholders[field]
            else:
                placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'paragraph-text contact-input contact_inputs '  # noqa
            self.fields[field].label = False


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('newsletter_email',)

        placeholders = {
            'newsletter_email': 'Email address'
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'newsletter_email': 'Email address'
        }

        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'paragraph-text contact-input newsletter_input'  # noqa
            self.fields[field].label = False
