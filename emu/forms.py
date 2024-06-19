from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('M', 'Mpesa')
)


class CheckoutForm(forms.Form):
    town = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield(required=False,
                                                                              widget=CountrySelectWidget(attrs={
                                                                                  'class': 'custom-select d-block w-100'
                                                                              }))
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



