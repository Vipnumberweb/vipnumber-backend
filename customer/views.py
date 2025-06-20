from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Customer
from .serializers import CustomerUpdateSerializer, CustomerSerializer

# Create your views here.

class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get customer profile details"""
        try:
            customer = request.user.customer_profile
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        """Update customer profile"""
        try:
            customer = request.user.customer_profile
            serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CustomerDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Deactivate customer account"""
        try:
            user = request.user
            customer = user.customer_profile

            # Deactivate the user instead of deleting
            user.is_active = False
            user.save()

            return Response(
                {"message": "Account deactivated successfully"}, 
                status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
