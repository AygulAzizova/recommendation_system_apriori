from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Tour
from .cart import Cart
from .forms import CartAddProductForm
@require_POST
def CartAdd(request, tour_id):
    cart = Cart(request)
    tour = get_object_or_404(Tour, id=tour_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(tour=tour, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartRemove(request, tour_id):
    cart = Cart(request)
    tour = get_object_or_404(Tour, id=tour_id)
    cart.remove(tour)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/detail.html', {'cart': cart})