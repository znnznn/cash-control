import requests
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Textarea
#from .views import exchange
from .models import *


class LoginUserForm(forms.Form):

    email = forms.EmailField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        fields = ('email', 'password')

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Incorrect Email or Incorrect Password")
        # if not user.check_password(password):
        #     raise forms.ValidationError("Incorrect Password")
        if not user.is_active:
            raise forms.ValidationError("User no longer Active")
        return super(LoginUserForm, self).clean(*args, **kwargs)


class UserSignUpForm(UserCreationForm): # add position
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
    code = forms.IntegerField(label='Verification code')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile', 'code')  # add position
        labels = {
            'code': 'Verification code',
        }

    def check_code(self):
        email = self.cleaned_data['email']
        ver_code = self.cleaned_data['code']
        member_code = 5555
        print(ver_code, member_code)
        if ver_code == member_code:
            return True
        return False


class UserDetailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class MYUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = ('is_active', 'is_admin')


class PayeeForm(forms.ModelForm):

    class Meta:
        model = Payee
        fields = ('email_payee', 'code')


#forms.BaseInlineFormSet

class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


def exchange(currency_code='USD'):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency_code}&json"
    my_url = requests.get(url)
    cookes = my_url.cookies
    my_url = requests.get(url, cookies=cookes)
    my_url = my_url.json()
    currency_rate = my_url[0]
    return currency_rate['rate']

class VoucherCreateForm(forms.ModelForm):
    rate = forms.CharField(initial=exchange(), disabled=True)

    class Meta:
        model = Transaction
        fields = ('user_id', 'description', 'debit',  'credit', 'cash_register_id', 'rate')
        labels = {
            'user_id': 'Payee name/Email     ',
            'cash_register_id': 'currency UAH ',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 25, 'rows': 2, 'placeholder': 'Office consumables' }),
        }

        # help_texts = {
        #     'description': 'Office consumables',
        # }


class VoucherConfirmForm(forms.ModelForm):
    rate = forms.CharField(initial=exchange(), disabled=True)

    class Meta:
        model = Transaction
        fields = ('user_id', 'description', 'debit',  'credit', 'cash_register_id', 'rate')

        labels = {
            'user_id': 'Payee name/Email     ',
            'cash_register_id': 'currency UAH ',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 25, 'rows': 2, 'placeholder': 'Office consumables'}),
        }

        # help_texts = {
        #     'description': 'Office consumables',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].disabled = True
        self.fields['debit'].disabled = True
        self.fields['credit'].disabled = True
        self.fields['cash_register_id'].disabled = True



class VoucherUpdateForm(forms.ModelForm):
    rate = forms.CharField(initial=exchange(), disabled=True)

    class Meta:
        model = Transaction
        fields = ('user_id', 'description', 'debit',  'credit', 'cash_register_id', 'rate')
        labels = {
            'user_id': 'Payee name/Email     ',
            'cash_register_id': 'currency UAH ',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 25, 'rows': 2, 'placeholder': 'Office consumables' }),
        }

        # help_texts = {
        #     'description': 'Office consumables',
        # }


p = VoucherConfirmForm(auto_id=False)
print(8888, p)





