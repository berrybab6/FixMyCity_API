import  random as rand
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User, PhoneOTP
from rest_framework.views import APIView
from .serializers import RegistorUserSerializer



def send_otp(phone):
    """
    This is a helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:
        key = rand.randint(999, 9999) 
        return key
    else:
        return False
        
      
    
    
class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone_number__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
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
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "u haven't set any phone number. Please do a POST request."
            })
            
            
            
            
class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

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
            
            


class Register(APIView):
    '''Takes phone  ,first name and lastname  and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', False)
        first_name = request.data.get('first_name', False)
        last_name = request.data.get('last_name', False)
        

        if phone_number and first_name and last_name:
            phone_number = str(phone_number)
            user = User.objects.filter(phone_number__iexact = phone_number)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated.'})
            else:
                old = PhoneOTP.objects.filter(phone_number__iexact = phone_number)
                if old.exists():
                    old = old.first()
                    validated = old.logged
                    if validated:
                        Temp_data = {'phone_number': phone_number, 
                                     'first_name': first_name,
                                     'last_name': last_name}

                        serializer = RegistorUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        # user.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'detail' : 'User has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })
                    




        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or password was not recieved in Post request'
            })

