from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import ShoeQuantityForm
from .models import Cart, CartProducts
from .utils import CartMixin
from started_app.models import Shoe


class CartView(CartMixin, generic.View):

    @staticmethod
    def auth_context(request):
        cart = Cart.objects.get(owner=request.user)
        products = cart.products.all()
        order_price = sum([product.price for product in products])
        return {
            'products': products,
            'order_price': order_price,
            'cart_number': len(products)
        }

    @staticmethod
    def non_auth_context(request):
        cart = request.session['cart']
        order_price = sum([int(i['fields']['price']) for i in cart.values()])
        return {
            'products': cart,
            'order_price': order_price,
            'cart_number': len(cart)
        }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.auth_context(request)
            template_path = 'cart/cart.html'
        else:
            context = self.non_auth_context(request)
            template_path = 'cart/session_cart.html'
        context = self.get_context_data(**context)
        return render(
            request,
            template_path,
            context
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = kwargs
        c_def = self.get_user_context()
        return {**context, **c_def}


class AddToCartView(CartMixin, generic.View):

    @staticmethod
    def add_if_auth(shoe, request, quantity, **kwargs):
        """
        if user is authenticated add item to cart or change its quantity in cart
        (if shoe already in user's cart)
        """
        cart = request.user.cart
        try:
            cart_product = CartProducts.objects.get(cart=cart, shoe=shoe)
            cart_product.quantity += quantity
            cart_product.save()
        except ObjectDoesNotExist:
            cart.products.add(shoe, through_defaults={'quantity': quantity})

    @staticmethod
    def add_if_not_auth(shoe, request, quantity, **kwargs):
        """Add item to cart if user is not authenticated"""
        cart = request.session['cart']
        if str(shoe.pk) in cart:
            cart[str(shoe.pk)]['quantity'] += quantity
        else:
            cart[str(shoe.pk)] = serializers.serialize('python', [shoe])[0]
            cart[str(shoe.pk)]['quantity'] = quantity
        request.session.modified = True

    def post(self, request,  *args, **kwargs):
        shoe = Shoe.objects.get(pk=kwargs['shoe_id'])
        form = ShoeQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if request.user.is_authenticated:
                self.add_if_auth(shoe, request, quantity)
            else:
                self.add_if_not_auth(shoe, request, quantity)
            return redirect('cart:cart')
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверные данные')
        return reverse(
            'started_app:show_shoe',
            args=(self.kwargs['shoe_id'])
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = kwargs
        c_def = self.get_user_context()
        return {**context, **c_def}


class DelFromCartView(SuccessMessageMixin, generic.View):

    def get(self, request, *args, **kwargs):
        shoe = Shoe.objects.get(pk=kwargs['shoe_id'])
        if request.user.is_authenticated:
            cart = Cart.objects.get(owner=request.user)
            cart.products.remove(shoe)
        else:
            cart = request.session['cart']
            cart.pop(str(kwargs['shoe_id']))
            request.session.modified = True
        return redirect('cart:cart')