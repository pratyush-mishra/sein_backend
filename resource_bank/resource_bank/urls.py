"""
URL configuration for resource_bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewSet, MessageViewSet, moderate_listing


router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('moderate/<str:token>/', moderate_listing, name='moderate_listing'),
    # Djoser authentication endpoints
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('auth/jwt/destroy/', CustomTokenDestroyView.as_view(), name='jwt_destroy'),
]

from users.views import CustomTokenObtainPairView, CustomTokenDestroyView

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
