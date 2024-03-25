from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user import CustomerSerializer
from user.models import Customer

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Customer registered successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = Customer.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # You can implement your own token-based authentication or use Django Rest Framework's token authentication here
        # For simplicity, let's assume the user is authenticated and return user data
        serializer = CustomerSerializer(user)
        return Response(serializer.data)
    


# In views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.urls import reverse
from user.models import Customer
import uuid

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = Customer.objects.filter(email=email).first()
        if user:
            # Generate a unique token (you can use UUID)
            token = uuid.uuid4().hex
            user.reset_token = token
            user.save()

            # Send email with reset link
            reset_link = request.build_absolute_uri(reverse('reset_password', kwargs={'token': token}))
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No user found with the provided email.'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    def post(self, request, token):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        user = Customer.objects.filter(reset_token=token).first()
        if user:
            user.set_password(password)
            user.reset_token = None
            user.save()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

# In urls.py