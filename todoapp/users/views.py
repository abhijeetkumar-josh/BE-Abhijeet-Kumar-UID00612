
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer  # adjust import as needed
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

class UserRegistrationAPIView(APIView):
    """
    success response format
    {
        "first_name": "Abhijeet",
        "last_name": "Kumar",
        "email": "abhi.kumar@josh.com",
        "password":""
    }
    """
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date_joined": user.date_joined,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """
    permission_classes=[AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'auth_token': token.key}, status=status.HTTP_200_OK)
