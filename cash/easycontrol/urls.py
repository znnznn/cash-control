from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', UserViews.as_view(), name='home'),
    path('user/', UserViews.as_view(), name='user_detail'),
    path('user/contacts/', UserViews.as_view(), name='user_contacts'),
    path('user/transaction/', UserViews.as_view(), name='transaction_list'),
    path('user/report/', UserViews.as_view(), name='report'),
    path('user/report/confirm/', UserViews.as_view(), name='report_confirm'),
    path('user/transaction/confirm/', UserViews.as_view(), name='transaction_confirm'),
    path('user/transaction/create/', UserViews.as_view(), name='transaction_create'),
    path('user/reception/volunteer/', UserViews.as_view(), name='volunteer_reception'),
    path('user/cash/register/<int:cash_register>', UserViews.as_view(), name='cash_register'),

]