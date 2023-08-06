from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from .serializer import MomoPaymentSerializer, MomoCallbackSerializer
from .momopay import MomoPayProcessor

# Create your views here.
def helloView(request):
    return HttpResponse('Hello, World!')


class MomoPaymentView(APIView):
    def post(self, request, id, *args, **kwargs):
        request_data = {'user': id}
        request_data.update(request.data)
        momoPaymentSerializer = MomoPaymentSerializer(data=request_data)
        if momoPaymentSerializer.is_valid():
            response = MomoPayProcessor(data=momoPaymentSerializer.validated_data).pay()
            return Response(response, status=HTTP_200_OK)
        return Response(momoPaymentSerializer.errors, status=HTTP_400_BAD_REQUEST)


class MomoPaymentCallbackView(APIView):
    def post(self, request):
        serializerResult = MomoCallbackSerializer(data=request.data)
        if serializerResult.is_valid(raise_exception=True):
            response = MomoPayProcessor(callback=serializerResult.validated_data).onCallback()
            return Response(response, status=HTTP_200_OK)
        return Response(serializerResult.errors, status=HTTP_400_BAD_REQUEST)