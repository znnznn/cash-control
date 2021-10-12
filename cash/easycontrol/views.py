from django.db.models import Sum, Case, When, Q, Max, ExpressionWrapper
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView

from .forms import *
from .models import *
# Create your views here.


class LoginUser(views.LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login')
    redirect_field_name = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ="Авторизація"
        return context

    def get_success_url(self):
        return reverse_lazy('transaction_list')


class UserViews(ListView):
    pass


class UserDetail(DetailView):
    form_class = UserDetail
    model = User
    template_name = 'registration/profile_user.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):

        print(10)
        queryset = User.objects.get(id=self.request.user.id)
        print(model_to_dict(queryset))
        return queryset

    # def get(self, request, *args, **kwargs):
    #     context = super().get(request, **kwargs)
    #     print(self.kwargs)
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f"Profile - {self.request.user.first_name}"
        return context


class TransactionList(ListView):
    model = Transaction
    template_name = 'registration/usertransaction.html'
    context_object_name = 'transaction'
    #allow_empty = True
    balance = ''

    def get_queryset(self):
        print(self.request.user)
        if not self.request.user.is_staff:
            self.balance = Transaction.objects.filter(user_id=self.request.user.id).aggregate(
                balance=Sum('debit') - Sum('credit')
            )
            queryset = Transaction.objects.filter(user_id=self.request.user.id)
        else:
            self.balance = Transaction.objects.all().aggregate(
                balance=Sum('debit') - Sum('credit')
            )
            queryset = Transaction.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        self.balance['balance'] = round(self.balance['balance'], 2)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chek transactions'
        context['balance'] = self.balance
        context['btn'] = self.request.user.is_staff
        print(context)
        print(context['transaction'])

        return context

