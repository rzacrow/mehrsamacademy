from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User, CustomToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'success': 'شما از حساب خود خارج شدید'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            check_exist = User.objects.filter(phone=request.data['phone']).exists()
            if check_exist:
                return Response({"error": "این شماره تلفن از قبل رزرو شده است"}, status=406)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Error" : "مشکلی در درخواست شما به وجود آمد"}, status=500)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class Login(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not phone or not password:
            return Response({'error': 'Phone and password must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize the phone number before passing it to authenticate
        normalized_phone = phone.strip().replace(" ", "")  # Or use the normalize_phone method

        user = authenticate(request, phone=normalized_phone, password=password)

        if user is not None:
            token, created = CustomToken.objects.get_or_create(user=user)
            return Response({'token': str(token.key)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid phone or password'}, status=status.HTTP_400_BAD_REQUEST)
