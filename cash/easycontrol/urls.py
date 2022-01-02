from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', TransactionList.as_view(), name='home'),
    path('user/detail', UserDetail.as_view(), name='user_detail'),
    path('user/delete', UserDetail.as_view(), name='del_profile'),
    path('user/contacts/', VoucherCreateView.as_view(), name='user_contacts'),  # not done
    path('user/transaction/', TransactionList.as_view(), name='transaction_list'),
    path('user/report/', VoucherCreateView.as_view(), name='report'),
    path('user/report/confirm/', VoucherCreateView.as_view(), name='report_confirm'),
    path('user/transaction/confirm/<int:pk>', VoucherDetailView.as_view(), name='transaction_confirm'),
    path('user/transaction/create/', VoucherCreateView.as_view(), name='transaction_create'),
    path('user/reception/payee/', PayeeView.as_view(), name='payee'),
    path('user/cash/register/<int:cash_register>', VoucherCreateView.as_view(), name='cash_register'),

]