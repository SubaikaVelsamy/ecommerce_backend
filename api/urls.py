from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, CategoryView, CategoryUpdateView, CategoryGetView, CategoryDeleteView, ProductView, ProductUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/logout/', LogoutView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/save_category/', CategoryView.as_view(), name='save_category'),
    path('auth/update_category/<int:pk>', CategoryUpdateView.as_view(), name='update_category'),
    path('auth/view_category/<int:pk>', CategoryGetView.as_view(), name='view_category'),
    path('auth/delete_category/<int:pk>', CategoryDeleteView.as_view(), name='delete_category'),
    path('auth/save_product/', ProductView.as_view(), name='save_product'),
    path('auth/update_product/<int:pk>', ProductUpdateView.as_view(), name='product_category'),
]
