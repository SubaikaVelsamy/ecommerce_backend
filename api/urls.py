from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, CategoryView, CategoryUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/logout/', LogoutView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/save_category/', CategoryView.as_view(), name='save_category'),
    path('auth/update_category/<int:pk>', CategoryUpdateView.as_view(), name='update_category'),
]
