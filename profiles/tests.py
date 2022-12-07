from django.test import TestCase

# Create your tests here.

def profile(request):
    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)