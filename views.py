from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from helper.helper import APIHandler

from .services import *
from .gateway_service import *

# Use this to charge
class Url_FastLaunch_Paynow(APIView):
    def get(self, request, charge_type, fastlaunch_no, email):
        pay_data = FASTLAUNCH_NEWEBPAY(fastlaunch_no, email,charge_type)

        if pay_data:
            return render(request, 'NEWEBPAY_pay.html', {'data':pay_data})
        else:
            return Response({'code': '000', 'data': 'Fail'})

# Use this to accept return data
class NEWEBPAY_Fastlaunch_ReturnData(APIView):
    def post(self, request):
        # Get transaction data
        data = request.data
        decrypt_data = NEWEBPAY_Decrypt(data['TradeInfo'])
        newebpay_decrypt_data = decrypt_data['Result']
        # Then do whatever you like to the return datas, like store transaction data into database
        return Response({'code': '000', 'data': 'Whatever'})
