from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, CategoryView, CategoryUpdateView, CategoryGetView, CategoryDeleteView, ProductView, ProductUpdateView, ProductDeleteView, ProductGetView, ProductListView, ProductDetailView, AddToCartView, CartClearView, CartView, CheckoutView, OrderStatusUpdateView
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
    path('auth/delete_product/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('auth/view_product/<int:pk>', ProductGetView.as_view(), name='view_product'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('clear_cart/<int:pk>/', CartClearView.as_view(), name='clear_cart'),
    path('view_cart/<int:cart_id>/', CartView.as_view(), name='view_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('update_order_status/<int:pk>/', OrderStatusUpdateView.as_view(), name='update_order_status'),


]
