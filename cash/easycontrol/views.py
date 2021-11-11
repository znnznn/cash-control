import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum, Case, When, Q, Max, ExpressionWrapper
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView

from .forms import *
from .models import *
# Create your views here.

from django.contrib.auth import authenticate, login


class LoginUser(views.FormView):

    initial = {'username': True}
    form_class = LoginUserForm
    template_name = 'registration/login.html'
    #success_url = reverse_lazy('transaction_list')
    #redirect_field_name = 'transaction_list'

    # def post(self, request, *args, **kwargs):
    #     print(self.request.POST)
    #     login(self.request, self.request.user)
    #     return super(LoginUser, self).post(request, **kwargs)

    def form_valid(self, form):
        print()
        #self.request.user = authenticate(request=self.request)
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        if email is not None and password:
            user = authenticate(self.request, email=email, password=password)
            if user is None:
                raise self.form_class.get_invalid_login_error()
            else:
                login(self.request, user)
        return super(LoginUser, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['title'] = "Authorization tab"
        return context

    def get_success_url(self):
        return reverse_lazy('transaction_list')


class VoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = VoucherCreateForm
    model = Transaction
    template_name = 'registration/voucher_create.html'
    context_object_name = 'voucher'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(VoucherCreateView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Petty Cash Voucher'
        context['btn'] = self.request.user.is_staff
        print(context)
        return context


class UserDetail(LoginRequiredMixin, UpdateView):
    form_class = UserDetailForm
    model = User
    template_name = 'registration/profile_user.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):

        queryset = User.objects.get(id=self.request.user.id)
        print(queryset)
        print(model_to_dict(queryset))
        print(11)
        return queryset

    # def get(self, request, *args, **kwargs):
    #     context = super().get(request, **kwargs)
    #     print(self.kwargs)
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f"Profile - {self.request.user.first_name}"
        print(444, context)
        return context


class SignUpView(CreateView):
    form_class = PayeeForm
    model = Payee
    template_name = 'registration/new_user.html'
    context_object_name = 'user'


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction()
    template_name = 'registration/usertransaction.html'
    context_object_name = 'transaction'
    #allow_empty = True
    balance = ''

    def get_queryset(self):
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
        print(self.balance)
        self.balance['balance'] = round(self.balance['balance'], 2) if self.balance else 0
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chek transactions'
        context['balance'] = self.balance
        context['btn'] = self.request.user.is_staff
        print(context)
        print(context['transaction'])

        return context


class PayeeView(LoginRequiredMixin, CreateView):

    form_class = PayeeForm
    template_name = 'registration/payee.html'
    context_object_name = 'payee'
    raise_exception = True
    success_url = reverse_lazy('transaction_list')
    #permission_required = 'transaction.can_edit'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(PayeeView, self).form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form_kwargs()
    #     print(7777, form)
    #     print(self.request.POST)
    #     # print(self.request.kwargs)
    #     return super(PayeeView, self).post(request, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        code = random.randrange(99999, 999999)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Payee | Counter Party'
        context['btn'] = self.request.user.is_staff
        context['code'] = code
        print(context)
        return context



