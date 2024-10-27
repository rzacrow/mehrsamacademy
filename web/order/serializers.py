from rest_framework import serializers
from .models import Order


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("user", "full_name", "status", "phone", "field", "degree", "title", "caption", "status", "ordered_at")