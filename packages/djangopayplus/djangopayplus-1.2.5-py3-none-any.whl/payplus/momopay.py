from django.conf import settings
from .models import MomoTransaction
import string, random, json, requests, hashlib
from .enum import NetworkTypes, StatusTypes
from django.core.serializers.json import DjangoJSONEncoder 

class MomoPayProcessor:
    
    def __init__(self, data=None, merchant=None, callback=None, *args, **kwargs):

        if data is not None:
            self.user = data['user']
            self.amount = data['amount']
            self.momo_number = data['customerNumber']
            self.network = data['payby']
            self.item_desc = data['item_desc']
            self.orderID = data.get('order_id', self.generateOrderID())
            self.network_name = NetworkTypes(data['payby']).name
        
        if callback is not None:
            self.callback = callback
            self.callback_url = callback.get('url', settings.PAYMENT_CALLBACK)
        
        self.merchant = merchant

    def pay(self):
        set_merchant = self.setMerchant()
        if set_merchant['status']:
            self.getPaymentPayload()
            try:
                self.momotrans = MomoTransaction.objects.create(
                    user = self.user,
                    amount = self.amount,
                    network = self.network,
                    msisdn = self.momo_number,
                    info_sent = self.payload,
                    order_id = self.orderID,
                    merchant_id = self.merchantID,
                    merchant_name = self.merchant_username,
                )
            except Exception as e:
                return {"status":False, "message":f"{e}"}
            self.response = requests.post(settings.PAYMENT_GATEWAY, data=json.dumps(self.payload, cls=DjangoJSONEncoder))
            self.momotrans.initial_callback = self.response.text
            self.momotrans.save()
            return self.parseMomoResponse()
        return set_merchant

        

    def parseMomoResponse(self):

        try:
            response = self.response.json()
            
            if response["Status"] == "Accepted":
                self.momotrans.ext_id = response["InvoiceNo"]
                self.momotrans.save()
                return {"status":True, "message":"Passed"}

            self.momotrans.final_callback = response.text
            
        except Exception as e:
            self.momotrans.final_callback = f"{e}"
        
        self.momotrans.status = StatusTypes.FAILED
        self.momotrans.save()
        return {"status": False, "message": self.response.text}

    
    def setMerchant(self):

        if self.merchant is not None:
            self.merchantID = self.merchant.get('id')
            self.merchant_username = self.merchant.get('username')
            self.merchant_password = self.merchant.get('password')
        else:
            try:
                self.merchantID = settings.PAYMENT_MERCHANT
                self.merchant_username = settings.PAYMENT_USERNAME
                self.merchant_password = settings.PAYMENT_PASSWORD
            except Exception as e:
                return {"status":False, "message":f"{e}"}
        return {"status":True}


    
    def generateOrderID(self):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(random.choices(alphabet, k=12))


    def getPaymentPayload(self):
        key = random.randint(1000, 9999)
        hash_merchant_password = hashlib.md5(self.merchant_password.encode("utf-8")).hexdigest()
        secret = hashlib.md5((self.merchant_username+str(key)+hash_merchant_password).encode("utf-8")).hexdigest()
        self.payload = {
            'merchant_id': self.merchantID,
            'secrete': secret,
            'key': key,
            'item_desc': self.item_desc,
            'callback': self.callback_url,
            'order_id': self.orderID,
            'customerName': self.user.username,
            'customerNumber': self.momo_number,
            'payby': self.network_name,
            'amount': self.amount,
        }
        if self.network == NetworkTypes.VODAFONE:
            self.payload["newVodaPayment"] = True



    def onCallback(self):
        if self.callback is not None:
        
            if self.callback["Status"] == "PAID":
                self.status_type = StatusTypes.COMPLETED
                status = True
            else:
                self.status_type = StatusTypes.FAILED
                status = False

            try:
                self.momotrans = MomoTransaction.objects.get(
                    order_id=self.callback["Order_id"],
                    ext_id=self.callback["InvoiceNo"],
                    status=StatusTypes.PENDING)
                self.momotrans.final_callback = json.dumps(self.callback , cls=DjangoJSONEncoder)
                self.momotrans.status = self.status_type                
                self.momotrans.save()
                return {"status":status, "transactionID":self.momotrans.id, "amount":self.momotrans.amount}
            except Exception as e:
                return {"status":False, "message":f"{e}"}