from django.shortcuts import render, reverse
from .forms import ContactForm

# Create your views here.


def index(request):
    contact_form = ContactForm(request.POST)
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
            form.save()
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [
                    email, settings.EMAIL_HOST_USER],
                    html_message=html_msg, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect(reverse('home'),
                            messages.success(request, 'Working'))

    context = {
        'contact_form': contact_form,
    }

    template = 'home/index.html'

    print(context)
    return render(request, template, context)
