from rest_framework import serializers
from .enum import NetworkTypes
from django.contrib.auth.models import User


class MomoPaymentSerializer(serializers.Serializer):

    user = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    item_desc = serializers.CharField(required=True)
    customerNumber = serializers.CharField(required=True)
    payby = serializers.CharField(required=True)
    

    def validate_item_desc(self, value):
        item_desc_len = len(value)
        if item_desc_len < 10  or item_desc_len > 24 :
            raise serializers.ValidationError("Item description should be greater than 9 but less than 25 characters")
        return value
    
    def validate_newVodaPayment(self, value):
        if type(value) is not bool:
            raise serializers.ValidationError("Boolean is required")
        return value

    
    def validate_customerNumber(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Number should be digits only")
        return value

    
    def validate_payby(self, network_name):
        try:
            payby = NetworkTypes.dichoices()[network_name.upper()]
            return payby
        except KeyError:
            raise serializers.ValidationError("Sorry, invalid network")


    def validate_user(self, userID):
        try:
            user = User.objects.get(pk=userID)
        except:
            raise serializers.ValidationError("Sorry, user does not exist")
        return user

class MomoCallbackSerializer(serializers.Serializer):
    Timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    Status = serializers.CharField()
    InvoiceNo = serializers.CharField()
    Order_id = serializers.CharField()