from payment.models import Invoice
from rest_framework import serializers
        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Invoice
        fields = ('id','created_at','status', 'amount', 'authority')