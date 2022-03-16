
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .serializers import LoginSerializer, UserSerializer
from .utils import Utils
from .models import SuperAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny, ]
    def post(self,request):
        data = request.data
        username = data['username']

        serializer = UserSerializer(data = data)
        
        # Check if the data is valid  and if not raise exception
        serializer.is_valid(raise_exception=True)

        # save to DB
        serializer.save()
        
        user = SuperAdmin.objects.get(username=username)
        token = Utils.encode_token(user)

        return Response({"data":serializer.data, "token":token})

class EditProfile(APIView):
    def put(self, request,id):
        user = SuperAdmin.objects.get(id=id)

        data = request.data.dict()

        serializer = UserSerializer(user, data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)




class LoginView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = Utils.authenticate_user(serializer.validated_data)
        serializedUser = UserSerializer(user)
        token = Utils.encode_token(user)
        
        return Response({"data":serializedUser.data, "token":token})



class TestView(APIView):
    def get(self, request):
        return Response({"Message":"TEST HOW RESPONSE WORKS"})