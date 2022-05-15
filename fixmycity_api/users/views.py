import  random as rand
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User, PhoneOTP
from rest_framework.views import APIView
from .serializers import RegistorUserSerializer  , LoginSerializer ,UpdateUserSerializer , ValidatePhoneSerializer , ValidateOtpSerializer
from rest_framework import permissions, generics, status
from django.contrib.auth import login
from accounts.utils import Utils
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
# from twilio.rest import Client
from rest_framework.permissions import IsAuthenticated
from permissions import IsCustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests


def send_otp(phone):
    """
    This is a helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:
        key = rand.randint(999, 9999) 
        key2 = " %d " % key
        print( key2)
        url = 'https://api.telda.com.et/api/write/SendOTP'

        request_type = "POST"
        print("this is ", url)
        data = {
            "phone": phone,
            "otp": 12344,
            "senderName" : "fixmycity",
            "remark" : "do not share this code with any one"
            
            } # post data
        print("this is json data", data)
        api_call = requests.request(method='POST', url= url, headers=
				{
                  'Content-Type': 'application/json; charset=UTF-8',
				  'Authorization': 'Basic TmUZkNo12kiDg2EDymmtRIfRhlaPi+W2MTAwMDk2Mjc4MjgwMA==',
            },
				json=data)
                
                
        print("response code",api_call)
        print(api_call.json())
        if api_call.status_code == 200:
            return key
        else:
            return False
       
        
    else:
        return False
    



        
      
    
    
class ValidatePhoneSendOTP(APIView):
    
    permission_classes = [AllowAny, ]
    serializer_class = ValidatePhoneSerializer
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''
    # phone_param_config = openapi.Parameter('phone_number' , in_=openapi.IN_QUERY , description="Description" , type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(request_body=ValidatePhoneSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone_number__iexact = phone)
            if user.exists():
                otp = send_otp(phone)
                # otp = 12345
                # key = rand.randint(999, 9999) 
               
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone_number__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone_number =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'message' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'message' : "OTP sending error. Please try after some time."
                            })
                
                return Response({
                    'status': True, 'message': 'Otp has been sent successfully please proceed to login.'
                })
            
                
                
                # return Response({'status': True, 'detail': 'Phone Number already exists , please proceed to Login'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone_number__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone_number =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'message' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'message' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'message': 'Otp has been sent successfully please verify otp.'
                })
        else:
            return Response({
                'status': 'False', 'message' : "u haven't set any phone number. Please do a POST request."
            })
            
            
            
            
class ValidateOTP(APIView):
    permission_classes = [AllowAny, ]

    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''
    serializer_class = ValidateOtpSerializer
 
    @swagger_auto_schema(request_body=ValidateOtpSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        otp_sent   = request.data.get('otp', False)

        if phone_number and otp_sent:
            old = PhoneOTP.objects.filter(phone_number__iexact = phone_number)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to registration'
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })
            
            
class Login(APIView):
    permission_classes = [AllowAny, ]
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''
    # serializer_class = LoginSerializer
 
    @swagger_auto_schema(request_body=ValidateOtpSerializer)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        otp_sent   = request.data.get('otp', False)

        if phone_number and otp_sent:
            old = PhoneOTP.objects.filter(phone_number__iexact = phone_number)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    phone_number = request.data['phone_number']
                    old = PhoneOTP.objects.filter(phone_number__iexact = phone_number)
                    if old.exists():
                        old = old.first()
                        serializer = LoginSerializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        user = Utils.authenticate_custome_user(serializer.validated_data)
                        print(user)
        # queryset = user
                        serializedUser = LoginSerializer(user)
                        token = Utils.encode_token(user)
                        old.delete()
                        return Response({"data":serializedUser.data, "token":token})
                    else:
                        return Response({
                            'status': False,
                            'message': 'Your otp was not verified earlier. Please go back and verify otp'

                        })

                    # return Response({
                    #     'status' : True, 
                    #     'detail' : 'OTP matched, kindly proceed to login'
                    # })
                else:
                    return Response({
                        'status' : False, 
                        'message' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'message' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'message' : 'Either phone or otp was not recieved in Post request'
            })
            
            

            
            


class Register(APIView):
    permission_classes = [AllowAny, ]
    '''Takes phone  ,first name and lastname  and creates a new user only if otp was verified and phone is new'''
    serializer_class = RegistorUserSerializer
 
    @swagger_auto_schema(request_body=RegistorUserSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        first_name = request.data.get('first_name', False)
        last_name = request.data.get('last_name', False)
        ProfileImage = request.data.get('ProfileImage' , False)
        

        if phone_number and first_name and last_name:
            phone_number = str(phone_number)
            user = User.objects.filter(phone_number__iexact = phone_number)
            if user.exists():
                return Response({'status': False, 'message': 'Phone Number already have account associated.'})
            else:
                old = PhoneOTP.objects.filter(phone_number__iexact = phone_number)
                if old.exists():
                    old = old.first()
                    validated = old.logged
                    if validated:
                        # Temp_data = {'phone_number': phone_number, 
                        #              'first_name': first_name,
                        #              'last_name': last_name,
                        #              'ProfileImage': ProfileImage
                        #              }

                        serializer = RegistorUserSerializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        
                        user = Utils.authenticate_custome_user(serializer.validated_data)
                        
                        print(user)
        # queryset = user
                        serializedUser = LoginSerializer(user)
                        token = Utils.encode_token(user)
        
        # return Response({"data":serializedUser.data, "token":token})
                        # user.save()

                        old.delete()
                        return Response({
                            'data' : serializedUser.data, 
                            'token' : token
                        })

                    else:
                        return Response({
                            'status': False,
                            'message': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : False,
                    'message' : 'Phone number not recognised. Kindly request a new otp with this number'
                })
                    




        else:
            return Response({
                'status' : 'False',
                'message' : 'Either first_name or last_name was not recieved in Post request'
            })
            
            
            

class EditProfile(APIView):
    permission_classes =  [IsAuthenticated, IsCustomUser]
    serializer_class = UpdateUserSerializer
 
    @swagger_auto_schema(request_body=UpdateUserSerializer)

    def patch(self, request, format=None):
        try:
            # exist then update
            profile = User.objects.get(id=request.user.id)
            serializer = UpdateUserSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    



    
  
        



