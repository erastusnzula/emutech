from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

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
