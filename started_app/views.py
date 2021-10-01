from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Shoe, Material
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


class ShowShoesView(DataMixin, generic.ListView):
    # Show all shoes
    template_name = 'started_app/shoes.html'
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context()
        return {**c_def, **context, }

    def get_queryset(self):
        return Shoe.objects.filter()


class FilterView(DataMixin, generic.ListView):
    template_name = 'started_app/shoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**c_def, **context, }

    def material_filter(self, sql_request, ):
        return sql_request.filter(
            material_id__name__in=self.request.GET.getlist('material')
        )

    def brand_filter(self, sql_request):
        return sql_request.filter(
            brand_id__name__in=self.request.GET.getlist('brand')
        )

    def price_filter(self, sql_request):
        return sql_request.filter(
            price__lte=self.request.GET.get('price-up-to')
        )

    def get_queryset(self):
        sql_req = Shoe.available_shoes.filter().select_related('material_id', 'brand_id')
        get_request = self.request.GET

        filter_auto_kwargs = {
            'material': 'material_id__name__in',
            'brand': 'brand_id__name__in',
            'price-up-to': 'price__lte',
            'price-from': 'price__gte'
        }

        for keyword, value in filter_auto_kwargs.items():
            if keyword in get_request and get_request.getlist(keyword):
                if 'price' not in keyword:
                    sql_req = sql_req.filter(**{value: get_request.getlist(keyword)})
                elif get_request.getlist(keyword)[0]:
                    sql_req = sql_req.filter(**{value: get_request.getlist(keyword)[0]})

        return sql_req


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


