from django.shortcuts import render, reverse
from .forms import ContactForm

# Create your views here.


def index(request):
    contact_form = ContactForm()
    context = {
		'contact_form': contact_form
	}
    return render(request, 'home/index.html', context)


def contact_form(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        if contact_form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': contact_form.cleaned_data['first_name'],
                'last_name': contact_form.cleaned_data['last_name'],
                'email': contact_form.cleaned_data['email_address'],
                'message': contact_form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [
                    email, settings.EMAIL_HOST_USER],
                    html_message=html_msg, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect(reverse('home'),
                            messages.success(request, 'Thank you for \
                                            your message, a copy of which\
                                            has been emailed to you. We will\
                                            get in touch with you as soon\
                                            as possible.'))

    context = {
        'contact_form': contact_form,
    }

    print("test")
    print(contact_form)
    return redirect(reverse('index'), context)
