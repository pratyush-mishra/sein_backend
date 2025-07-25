"""
URL configuration for resource_bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewSet, MessageViewSet, moderate_listing
from users.views import moderate_user

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('moderate/<str:token>/', moderate_listing, name='moderate_listing'),
    path('moderate_user/<str:token>/', moderate_user, name='moderate_user'),
    # Djoser authentication endpoints (includes JWT endpoints)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)