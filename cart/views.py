from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from started_app.utils import DataMixin
from .forms import ShoeQuantityForm
from .models import Cart, CartProducts, Order
from .utils import CartMixin
from started_app.models import Shoe


class CartView(CartMixin, generic.View):

    @staticmethod
    def auth_context(request):
        cart = Cart.objects.get(owner=request.user)
        products = cart.products.all()
        order_price = sum([
            product.price * product.cartproducts_set.get(cart=cart).quantity for product in products
        ])
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


class OrderView(DataMixin, generic.DetailView):
    # Page after adding order: show details of order
    template_name = 'cart/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        order_price = 0
        for thing in self.object.orderproduct_set.all():
            order_price += thing.quantity * thing.price
        context.update(
            {'order_price': order_price}
        )
        return {**context, **c_def}

    def get_queryset(self):
        return Order.objects.filter(pk=self.kwargs['pk'])


class OrderCreate(DataMixin, generic.CreateView):
    # Create order
    model = Order
    fields = ['comment']
    template_name = 'cart/add_order.html'

    def form_valid(self, form):
        # Link order with user
        form.instance.user = self.request.user
        cart = self.request.user.cart
        form.save()
        for product in cart.products.all():
            form.instance.shoes.add(
                product,
                through_defaults={
                    'quantity': CartProducts.objects.get(shoe=product, cart=cart).quantity,
                    'price': product.price
                }
            )
        # clean cart after creating order
        cart.cartproducts_set.all().delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cart:order', args=(self.object.pk, ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}
