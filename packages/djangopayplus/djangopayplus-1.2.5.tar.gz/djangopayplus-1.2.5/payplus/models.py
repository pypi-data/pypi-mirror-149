from django.db import models
from django.conf import settings
from . import enum


class MomoTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    network = models.IntegerField(choices=enum.NetworkTypes.choices())
    msisdn = models.CharField(max_length=20)
    merchant_id = models.CharField(max_length=20)
    merchant_name = models.CharField(max_length=100)
    status = models.IntegerField(choices=enum.StatusTypes.choices(), default=enum.StatusTypes.PENDING)
    info_sent = models.TextField()
    initial_callback = models.CharField(max_length=255, null=True)
    final_callback = models.CharField(max_length=255, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=50, unique=True)
    ext_id = models.CharField(max_length=50,null=True)