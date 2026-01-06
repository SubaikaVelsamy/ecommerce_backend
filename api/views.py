# api/views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, CategorySerializer, ProductSerializer, ProductListSerializer, ProductDetailSerializer, CartSerializer, CartItemSerializer, CartViewSerializer, OrderSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrSuperAdmin
from django.shortcuts import get_object_or_404
from .models import Category, Product, Cart, CartItem, Order, OrderItem   
import json
from django.db import transaction
from .tasks import send_order_update_email



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
        })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )
    
class CategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryGetView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'   # matches URL

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        return Response({
            "name": category.name,
            "description": category.description
        })
    
class CategoryDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        # get the object
        instance = self.get_object()
        # delete it
        self.perform_destroy(instance)
        # return custom response
        return Response(
            {"detail": f"Category '{instance.name}' deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        # get the object
        instance = self.get_object()
        # delete it
        self.perform_destroy(instance)
        # return custom response
        return Response(
            {"detail": f"Product '{instance.name}' deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class ProductGetView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'pk'   # matches URL

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        return Response({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.price,
            "category_name": product.category.name
        })

class ProductListView(ListAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.user.id
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # 1️⃣ Get or create cart
        cart, cart_created = Cart.objects.get_or_create(user_id=user_id)

        # 2️⃣ Add or update cart item
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id
        )

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        # 3️⃣ Return cart_id
        return Response({
            "message": "Item added to cart",
            "cart_id": cart.id,
            "cart_created": cart_created,
            "product_id": product_id,
            "quantity": cart_item.quantity
        }, status=status.HTTP_200_OK)
    
class CartClearView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        # get the object
        instance = self.get_object()
        # delete it
        self.perform_destroy(instance)
        # return custom response
        return Response(
            {"detail": f"Cart cleared successfully."},
            status=status.HTTP_200_OK
        )
    
class CartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartViewSerializer

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(
            cart_id=self.kwargs['cart_id'],
            cart__user_id=self.request.user.id
        )
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user_id = request.user.id

        # 1️⃣ Get cart
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            return Response(
                {"detail": "Cart not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Calculate total
        total_price = 0
        product_map = {}

        for item in cart_items:
            product = Product.objects.get(id=item.product_id)
            item_total = product.price * item.quantity
            total_price += item_total
            product_map[item.product_id] = product.price

        # 3️⃣ Create order
        order = Order.objects.create(
            user_id=user_id,
            total_price=total_price,
            status='pending'
        )

        # 4️⃣ Create order items
        order_items = [
            OrderItem(
                order=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product_map[item.product_id]
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # 5️⃣ Clear cart
        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_price": total_price,
            "status": order.status
        }, status=status.HTTP_201_CREATED)


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    """ def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            send_order_update_email.delay(order.id, "subaika.nadar@luminad.com", order.status)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)