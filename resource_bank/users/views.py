from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from djoser.views import TokenDestroyView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # Use True in production with HTTPS
                samesite='Lax',
                max_age=3600 # Example: 1 hour
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,  # Use True in production with HTTPS
                samesite='Lax',
                max_age=86400 * 7 # Example: 7 days
            )
            # Remove tokens from the response body if you only want them in cookies
            del response.data['access']
            del response.data['refresh']
        return response

class CustomTokenDestroyView(TokenDestroyView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
