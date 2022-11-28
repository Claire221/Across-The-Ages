from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are no items in your bag")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'

    contect = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51M94xIHVGSxAtM8PTGUbFhFxZhojInqWSF8Jc7fIaEvholWwNXvqnufyFqM53uxge740d3idxHneOn4E3tk5LUEb00EJtMqpN7',
        'client_sercret': 'test secret'
    }

    return render(request, template, contect)