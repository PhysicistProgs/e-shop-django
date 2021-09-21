from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404, render
from .models import Order, Shoe, Cart
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from .utils import DataMixin


class IndexView(DataMixin, generic.ListView):
    # Homepage
    template_name = 'started_app/index.html'
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


class ThanksView(generic.DetailView):
    # Page after adding order
    template_name = 'started_app/thanks.html'
    model = User


class ShowUsersView(generic.ListView):
    # Show all users
    template_name = 'started_app/users.html'
    model = User


class UserInfoView(generic.DetailView):
    # Show user info
    template_name = 'started_app/user_info.html'
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['order_list'] = instance.order_set.all()
        return context


class ShowShoesView(DataMixin, generic.ListView):
    # Show all shoes
    template_name = 'started_app/shoes.html'
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context()
        return {**c_def, **context, }


class ShoeInfoView(DataMixin, generic.DetailView):
    # Show shoe info
    template_name = 'started_app/shoe_info.html'
    model = Shoe
    context_object_name = "shoe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context()
        return {**c_def, **context, }


class RegisterUserView(SuccessMessageMixin,DataMixin, generic.CreateView):
    form_class = UserCreationForm
    template_name = 'started_app/register.html'
    success_url = reverse_lazy('login')
    success_message = "Регистрация прошла успешно"


class LoginUserView(SuccessMessageMixin, DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'started_app/login.html'
    success_url = reverse_lazy('index')
    success_message = 'Выполнен вход в систему'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


class OrderCreate(generic.CreateView):
    # Create order
    model = Order
    fields = ['comment']
    template_name = 'started_app/add_order.html'

    def form_valid(self, form):
        # Link order with user
        form.instance.user_id = User.objects.get(pk=self.kwargs.get('pk'))
        Cart.objects.create(owner=form.instance.user_id)
        return super().form_valid(form)

    def get_success_url(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return reverse('thanks', args=(user.pk, ))


class CartView(DataMixin, generic.View):

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(owner=request.user)
        products = cart.products.all()
        order_price = sum([product.price for product in products])
        context = {
            'cart': cart,
            'products': products,
            'order_price': order_price,
            'cart_number': len(products)
        }
        return render(
            request,
            'started_app/cart.html',
            context
        )


class AddToCartView(generic.View):

    def get(self, request,  *args, **kwargs):
        print("kwargs:", kwargs)
        shoe = Shoe.objects.get(pk=kwargs['shoe_id'])
        cart = Cart.objects.get(owner=request.user)
        cart.products.add(shoe)
        return redirect('cart')
