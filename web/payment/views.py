from django.shortcuts import redirect
from .models import Invoice
import requests, json
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from payment.serializers import InvoiceSerializer
from order.models import Order



class VerifyPayment(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        try:
            status = request.GET.get('Status')
            print("Status: ", status)
            authority = request.GET.get('Authority')

            if status == "OK":
                try:
                    invoice = Invoice.objects.get(authority=authority)
                except:
                    return Response({"error" : "سفارشی با این کد رهگیری پیدا نشد! در صورت پرداخت، این موضوع را با پشتیبانی در میان بگذارید"}, status=404)


                if invoice.status != "Active":
                    return redirect("/payment-error")

                invoice.status = "Paid"
                invoice.save()
                order = Order.objects.get(id=invoice.order)
                order.status = "C"
                order.save()
                return redirect("/payment-success")
            
            return redirect("/payment-error")
        except:
            return redirect("/payment-error")



class GetAuthority(APIView):
    permissions_classes = [IsAuthenticated]

    def post(self, request):
        order = None

        try:
            order_id = request.POST["order"]
            order = Order.objects.get(id=order_id)
        except:
            return Response({"error" : "سفارش مورد نظر پیدا نشد!"}, status=406)

        description = "Mehrsam Academy"
        mobile = request.POST.get("mobile", "Null")
        email = request.POST.get("email", "Null")
        amount = request.POST.get("amount", 0)
        
        
        data = {
            "merchant_id" : "03418ead-550f-43e3-ae3a-37f4d9d85a2a",
            "amount" : amount,
            "description" : description,
            "callback_url" : 'http://127.0.0.1/api/payment/verify/',
            "metadata" : {
                "mobile" : mobile,
                "email" : email,
            },
            "order_id" : order_id
        }

        data = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Accept" : "application/json"
        }

        url = "https://api.zarinpal.com/pg/v4/payment/request.json"
        result = requests.post(url=url, headers=headers, data=data)


        if result.status_code == 200:
            result = result.json()
    
        try:
            if result['data']['code'] != 100:
                return Response({"error" : "مشکلی در ارتباط با درگاه پرداخت بوجود آمد. لطفا دوباره امتحان کنید و درصورت تکرار آن، این موضوع را به پشتیبانی اطلاع دهید"}, status=503)
        except:
            return Response({"error" : "مشکلی در ارتباط با درگاه پرداخت بوجود آمد. لطفا دوباره امتحان کنید و درصورت تکرار آن، این موضوع را به پشتیبانی اطلاع دهید"}, status=503)

        authority = result['data']['authority']

        url = f"https://www.zarinpal.com/pg/StartPay/{authority}"
        data = json.loads(data)
        Invoice.objects.create(amount=data['amount'] ,status="Active", order=order, authority=authority, url=url)
        order.status = "B"
        order.save()
        return Response({"success" : "فاکتور پرداخت موردنظر ایجاد گردید!"}, status=200)
    

class InvoiceListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        return Invoice.objects.filter(order__user=user).order_by('-created_at')