from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Shoe
from cart.forms import ShoeQuantityForm
from cart.models import CartProducts, Order
from .utils import DataMixin


class IndexView(DataMixin, generic.ListView):
    # Homepage
    template_name = 'started_app/index.html'
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


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
    context_object_name = 'shoe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['form'] = ShoeQuantityForm
        return {**c_def, **context, }


class RegisterUserView(SuccessMessageMixin, DataMixin,  generic.CreateView):
    form_class = UserCreationForm
    template_name = 'started_app/register.html'
    success_url = reverse_lazy('started_app:login')
    success_message = "Регистрация прошла успешно"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


class LoginUserView(SuccessMessageMixin, DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'started_app/login.html'
    success_url = reverse_lazy('started_app:index')
    success_message = 'Выполнен вход в систему'

    def get_success_url(self):
        return reverse_lazy('started_app:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


def logout_user(request):
    logout(request)
    return redirect('started_app:login')


class OrderView(DataMixin, generic.DetailView):
    # Page after adding order
    template_name = 'cart/thanks.html'
    model = Order

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


class OrderCreate(DataMixin, generic.CreateView):
    # Create order
    model = Order
    fields = ['comment']
    template_name = 'cart/add_order.html'
    # success_url = reverse_lazy('thanks')

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
        return reverse('started_app:thanks', args=(self.object.pk, ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}
