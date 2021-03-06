from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.API import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('me/', views.current_user_details, name='current_user_details'),
    path('<str:username>/', views.user_details, name='user_details'),
    path('password/change/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
]

