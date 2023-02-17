from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, NewsletterForm
from .models import Newsletter
from django.conf import settings


def index(request):
    newsletter = NewsletterForm()

    contact_form = ContactForm(request.POST or None)

    if request.method == 'POST':

        if contact_form.is_valid():
            contact_form.save()
            subject = "Website Inquiry"
            body = (
                'Thank you for contacting Acros the Ages, '
                'here is a copy of your email \n\n'
                f'First Name: {request.POST.get("first_name")}'
                f'\nLast Name: {request.POST.get("last_name")}'
                f'\nEmail: {request.POST.get("email")}'
                f'\nMessage: {request.POST.get("message")}'
            )
            email = request.POST.get("email")
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, settings.DEFAULT_FROM_EMAIL]
                )
                return redirect(
                    reverse('home'),
                    messages.success(
                        request,
                        'Your message has been sent, '
                        'someone will be intouch soon.'))
            except Exception as e:
                return redirect(
                    reverse('home'),
                    messages.error(
                        request,
                        'Something went wrong, Please try again.'
                    )
                )
        else:
            return redirect(
                reverse('home'),
                messages.error(
                    request,
                    'Something went wrong, Please try again.'
                )
            )

    context = {
        'contact_form': contact_form,
        'newsletter': newsletter
    }

    template = 'home/index.html'
    return render(request, template, context)


def newsletter(request):
    newsletter = NewsletterForm(request.POST or None)
    if request.method == 'POST':
        if newsletter.is_valid():
            email = request.POST.get("newsletter_email")
            existing_email = Newsletter.objects.filter(newsletter_email=email).exists()  # noqa
            if not existing_email:
                newsletter.save()
                subject = "Newsletter sign up"
                message = (
                    'You have successfully signed up for Across the Ages '
                    'newsletter '
                    'where you will be notified of new products and sales.')
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email]
                    )
                    return redirect(
                        reverse('home'),
                        messages.success(
                            request,
                            'You have successfuly signed up to our newsletter!'))  # noqa
                except Exception as e:
                    return redirect(
                        reverse('home'),
                        messages.error(
                            request,
                            'Something went wrong, Please try again.'
                        )
                    )
            else:
                return redirect(
                    reverse('home'),
                    messages.success(
                        request,
                        'You are already subscribed to our newsletter!')) 
    context = {
        'newsletter': newsletter,
    }

    template = 'home/index.html'
    return render(request, template, context)
