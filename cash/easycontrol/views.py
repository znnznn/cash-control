import random

import requests
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Sum, Case, When, Q, Max, ExpressionWrapper
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render, get_object_or_404
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
                form.form_invalid()
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
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        #form.instance.user_id = self.request.user
        return super(VoucherCreateView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Petty Cash Voucher'
        context['btn'] = self.request.user.is_staff
        print(context)
        context['currency_data'] = exchange()
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
    form_class = UserSignUpForm
    model = User
    template_name = 'registration/new_user1.html'
    context_object_name = 'user'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if form.check_code():
            self.object = form.save(form)
            return super().form_valid(form)
        form.add_error('code', 'wrong verification code')
        return super().form_invalid(form)


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction()
    template_name = 'registration/usertransaction.html'
    context_object_name = 'transaction'
    #allow_empty = True
    paginate_by = 10
    balance = ''
    redirect_field_name = 'login'

    # def test_func(self): # UserPassesTestMixin
    #
    #     print('test_func', self.request.user.is_staff)
    #     return self.request.user.is_staff

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
        self.balance['balance'] = round(self.balance['balance'], 2) if self.balance['balance'] else 0
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chek transactions'
        context['balance'] = self.balance
        context['btn'] = self.request.user.is_staff

        print(context['transaction'])

        return context


class VoucherDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = VoucherConfirmForm
    model = Transaction
    template_name = 'registration/user_transaction_confirm.html'
    context_object_name = 'transaction'
    allow_empty = True
    balance = ''
    redirect_field_name = 'login'

    def test_func(self):  # UserPassesTestMixin
        print('test_func', self.kwargs)
        pk = self.kwargs.get('pk')

        transaction = get_object_or_404(Transaction, pk=pk)
        if transaction.user_id == self.request.user or self.request.user.is_staff:
            return True
        return False

    # def get_object(self, queryset=None):
    #     print(self.kwargs)
    #     print(self.request.POST)
    #     pk = self.request.GET.get('pk') or self.request.POST.get('pk')
    #     obj = Transaction.objects.get(id=pk)
    #     print(obj)
    #     print(model_to_dict(obj))
    #     print(11)
    #     return obj
    #
    # def get_queryset(self):
    #     pk = self.request.GET.get('pk') or self.request.POST.get('pk')
    #     queryset = Transaction.objects.filter(pk=pk)
    #     if queryset.user_id == self.request.user.id:
    #         return queryset
    #     raise Http404(("No %(verbose_name)s found matching the query") %
    #                   {'verbose_name': queryset.model._meta.verbose_name})

    def get(self, request, *args, **kwargs):
        self.form_class = self.get_for(self.request.user.is_staff)
        print('GET', self.request.GET.get('pk'))
        #self.kwargs['pk'] = int(self.request.GET.get('pk'))
        # self.kwargs['object'] = self.get_object()
        # print(self.kwargs['object'])
        return super(VoucherDetailView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if form.check():
            self.object = form.save(form)
            return super().form_valid(form)
        form.add_error('user_id', 'no permissions')
        return super().form_invalid(form)

    def get_for(self, is_staff):
        if is_staff:
            return VoucherUpdateForm
        else:
            return VoucherConfirmForm

    def post(self, request, *args, **kwargs):
        self.kwargs['pk'] = int(self.request.POST.get('pk'))
        # self.object = self.get_object()
        #form = super(Transaction, self).get_form(self.form_class)
        return super(VoucherDetailView, self).post(request, *args, **kwargs)


class PayeeView(LoginRequiredMixin, CreateView):

    form_class = PayeeForm
    template_name = 'registration/payee.html'
    context_object_name = 'payee'
    raise_exception = True
    success_url = reverse_lazy('transaction_list')
    #permission_required = 'transaction.can_edit'

    def post(self, request, *args, **kwargs):
        self.code = random.randrange(99999, 999999)
        email_payee = self.request.POST.get('email_payee')
        try:
            payee_user = User.objects.get(email=email_payee)
        except:
            try:
                send_mail(
                    'Password recovery',
                    f"code for recovery: {self.code}",
                    'znnintway@gmail.com',  # from settings
                    [email_payee],
                    fail_silently=False,
                )
            except:
                form = self.get_form(self.form_class)
                form.add_error('email_payee', 'Wrong email')
        return super(PayeeView, self).post(request, **kwargs)

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.code = self.code
        return super(PayeeView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Payee | Counter Party'
        context['btn'] = self.request.user.is_staff
        return context


class CashRegisterDetailView(LoginRequiredMixin, DetailView):
    pass


class CashRegisterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    pass





def exchange(currency_code='USD') -> dict:
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency_code}&json"
    my_url = requests.get(url)
    cookes = my_url.cookies
    my_url = requests.get(url, cookies=cookes)
    my_url = my_url.json()
    currency_rate = my_url[0]
    return currency_rate



