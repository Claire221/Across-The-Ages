from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, Newsletter
from django.conf import settings


def index(request):
    newsletter = Newsletter()

    contact_form = ContactForm(request.POST or None)

    if request.method == 'POST':

        if contact_form.is_valid():
            contact_form.save()
            subject = "Website Inquiry"
            body = (
                f'First Name: {request.POST.get("first_name")}'
                f'\nLast Name: {request.POST.get("last_name")}'
                f'\nEmail: {request.POST.get("email")}'
                f'\nMessage: {request.POST.get("message")}'
            )
            email = request.POST.get("email")
            try:
                send_mail(
                    subject,
                    message,
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
    newsletter = Newsletter(request.POST or None)
    if request.method == 'POST':
        if newsletter.is_valid():
            newsletter.save()
            subject = "Newsletter sign up"
            message = (
                'You have successfully signed up for Across the Ages '
                'newsletter '
                'where you will be notified of new products and sales.')
            email = request.POST.get("newsletter_email")
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
                        'You have successfuly signed up to out newsletter!'))
            except Exception as e:
                print(e)
                return redirect(
                    reverse('home'),
                    messages.error(
                        request,
                        'Something went wrong, Please try again.'
                    )
                )
    context = {
        'newsletter': newsletter,
    }

    template = 'home/index.html'
    return render(request, template, context)
