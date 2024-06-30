import base64
from datetime import datetime

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth


def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" \
        if settings.MPESA_ENVIRONMENT == 'sandbox' \
        else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response.raise_for_status()
    access_token = response.json().get('access_token')
    return access_token


def initiate_stk_push(mobile_number, amount):
    access_token = get_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" \
        if settings.MPESA_ENVIRONMENT == 'sandbox' \
        else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    initiation_time = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + initiation_time).encode('utf-8')).decode('utf-8')
    data = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": initiation_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": mobile_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": mobile_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": 'EMU',
        "TransactionDesc": 'EMU Payments'
    }

    response = requests.post(api_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def get_conversion_rate(amount):
    api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
    data = requests.get(api_url).json()
    currencies = data['rates']
    from_ = 'USD'
    to = 'KES'
    get_amount = float(amount)
    get_amount = get_amount / currencies[from_]
    get_amount = round(get_amount * currencies[to], 4)
    print(currencies[to])
    return int(get_amount)
