from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from .models import Order, Shoe
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    # Homepage
    template_name = 'started_app/index.html'
    model = User


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


class ShowShoesView(generic.ListView):
    # Show all shoes
    template_name = 'started_app/shoes.html'
    model = Shoe


class ShoeInfoView(generic.DetailView):
    # Show shoe info
    template_name = 'started_app/shoe_info.html'
    model = Shoe
    context_object_name = "shoe"


class RegisterUserView(SuccessMessageMixin, generic.CreateView):
    form_class = UserCreationForm
    template_name = 'started_app/register.html'
    success_url = reverse_lazy('login')
    success_message = "Регистрация прошла успешно"


class LoginUserView(SuccessMessageMixin, LoginView):
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
        return super().form_valid(form)

    def get_success_url(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return reverse('thanks', args=(user.pk, ))
