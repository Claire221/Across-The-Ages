from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, Newsletter
from django.conf import settings

# Create your views here.


def index(request):
    newsletter = Newsletter(request.POST)

    # Contact form code
    contact_form = ContactForm()

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'message': request.POST['message']
        }

        contact_form = ContactForm(form_data)

        if contact_form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': contact_form.cleaned_data['first_name'],
                'last_name': contact_form.cleaned_data['last_name'],
                'email': contact_form.cleaned_data['email'],
                'message': contact_form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            contact_form.save()
            try:
                email = contact_form.cleaned_data['email']
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                    email, settings.DEFAULT_FROM_EMAIL])
                return redirect(reverse('home'),
                                messages.success(request,
                                'Your message has been sent, someone will be intouch soon.')
                                )
            except Exception as e:
                return redirect(reverse('home'),
                                messages.error(request,
                                'Something went wrong, Please try again.')
                                )
    context = {
        'contact_form': contact_form,
        'newsletter': newsletter
    }

    template = 'home/index.html'
    return render(request, template, context)


def newsletter(request):
    newsletter = Newsletter()
    if request.method == 'POST':
        newsletter_data = {
            'email': request.POST['email']
        }

        newsletter = Newsletter(newsletter_data)

        if newsletter.is_valid():
            email = newsletter.cleaned_data['email']
            newsletter.save()
            subject = "Newsletter sign up"
            message = "You have successfully signed up for Across the Ages newsletter where you will be notified of new products and sales."
            try:
                email = newsletter.cleaned_data['email']
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                    email, settings.DEFAULT_FROM_EMAIL])
                return redirect(reverse('home'),
                                messages.success(
                                request,
                                'You have successfuly signed up to out newsletter!')
                                )
            except Exception as e:
                print(e)
                return redirect(reverse('home'),
                                messages.error(request,
                                'Something went wrong, Please try again.')
                                )
    context = {
        'newsletter': newsletter,
    }

    template = 'home/index.html'
    return render(request, template, context)
