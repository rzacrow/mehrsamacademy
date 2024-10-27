from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrderSerializers
from rest_framework.permissions import IsAuthenticated
from .models import Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class SubmitOrder(APIView):
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        response_serializer = OrderSerializers(instance)
        self.response_data = response_serializer.data

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        response = super().create(request, *args, **kwargs)
        response.data = self.response_data
        return response
    

class OrderChange(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Use `partial=True` to allow partial updates
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)