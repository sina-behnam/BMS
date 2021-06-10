from django.urls import path, include
from users.views import UserCreate, UserList, UserSignIn, UserUpdate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', UserList.as_view()),
    path('update/<int:pk>', UserUpdate.as_view()),
    path('signup/', UserCreate.as_view()),
    path('signin/', UserSignIn.as_view()),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]