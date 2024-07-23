from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

PAYMENT_OPTION = (
    ('M', 'Mpesa'),
    ('P', 'PayPal'),
    ('S', 'Stripe'),
)


class CheckoutForm(forms.Form):
    town = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield(required=False,
                                                                     widget=CountrySelectWidget())
    zip_code = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTION)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promotion code',
        'aria - label': "Recipient's username",
        'aria - describedby': "basic-addon2"
    }))
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter a valid Email Address")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=255, help_text="Enter Your Username")
    password = forms.CharField(max_length=255,widget=forms.PasswordInput, help_text="Enter Your Password")
    class Meta:
        model = User
        fields = ('username', 'password')
    