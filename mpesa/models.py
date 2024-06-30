from django.db import models


class STKPushTransaction(models.Model):
    merchant_id = models.CharField(max_length=255)
    checkout_id = models.CharField(max_length=255)
    result_code = models.CharField(max_length=255)
    result_description = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    transaction_date = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
