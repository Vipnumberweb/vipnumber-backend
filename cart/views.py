from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer
from customer.models import Customer
from number.models import Number
import logging

logger = logging.getLogger(__name__)

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request):
        """List all items in the user's cart"""
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = Cart.objects.filter(customer=customer)
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a number to cart"""
        try:
            customer = request.user.customer_profile
            
            # Log the incoming request data
            logger.info(f"Cart POST request data: {request.data}")
            
            # First validate the number exists
            number_id = request.data.get('number')
            if not number_id:
                return Response({"error": "Number ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            number = get_object_or_404(Number, id=number_id)
            if number.is_sold:
                logger.error(f"Number {number.id} is already sold")
                return Response(
                    {"error": "Number is already sold"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if number is already in cart
            if Cart.objects.filter(customer=customer, number=number).exists():
                logger.error(f"Number {number.id} is already in cart for customer {customer.id}")
                return Response(
                    {"error": "Number already in cart"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create serializer with validated data
            serializer = self.serializer_class(
                data={'customer': customer.id, 'number': number.id},
                context={'request': request}
            )
            
            if serializer.is_valid():
                # Save the cart item
                cart_item = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.error(f"Invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Customer.DoesNotExist:
            logger.error(f"Customer profile not found for user {request.user.id}")
            return Response(
                {"error": "Customer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error adding to cart: {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, number_id=None):
        """Remove an item from cart"""
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            print("Customer profile not found")
            return Response({"error": "Customer profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not number_id:
            return Response({"error": "Number ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(Cart, customer=customer, number__id=number_id)
        
        print(cart_item)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
