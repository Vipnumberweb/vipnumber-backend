from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Vendor
from authentication.models import VN_User
from authentication.serializers import UserRegistrationSerializer
from .serializers import *

class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

    def get_queryset(self):
        """Ensure the user can only access their own vendor profile"""
        return Vendor.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override create method to prevent duplicate vendor profiles"""
        if Vendor.objects.filter(user=request.user).exists():
            return Response({"error": "Vendor profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Save the vendor profile without explicitly passing user"""
        serializer.save()  # Don't pass `user=self.request.user`, serializer handles it.


class AllVendorsView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = AllVendorSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_context_data(self, **kwargs):
        return Vendor.objects.all()

class VendorUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    lookup_field = 'id'

    def get_object(self):
        """Ensure vendors can only update their own profile"""
        obj = super().get_object()
        if not self.request.user.is_staff and obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to edit this vendor profile")
        return obj

    def post(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Remove is_approved from request data to prevent unauthorized changes
        request_data = request.data.copy()
        request_data.pop('is_approved', None)
        
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class VendorApprovalView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        vendor = self.get_object()
        vendor.is_approved = True
        vendor.save()
        serializer = self.get_serializer(vendor)
        return Response({
            "message": "Vendor approved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class UnapprovedVendorsView(generics.ListAPIView):
    serializer_class = AllVendorSerializers
    permission_classes = [permissions.IsAdminUser]  # Only admin can see unapproved vendors
    
    def get_queryset(self):
        return Vendor.objects.filter(is_approved=False)

class AdminCreateVendorView(generics.CreateAPIView):
    serializer_class = AdminCreateVendorSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()

        return Response({
            "message": "Vendor created and approved successfully.",
            "vendor_id": str(vendor.id),
            "user_id": str(vendor.user.id),
            "email": vendor.user.email,
            "phone": vendor.user.phone,
            "is_approved": vendor.is_approved
        }, status=status.HTTP_201_CREATED)


class AdminUpdateVendorView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = AdminUpdateVendorSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'  # ensure this matches your URL pattern

    def update(self, request, *args, **kwargs):
        print("Update request data:", request.data)
        return super().update(request, *args, **kwargs)
    

class AdminVendorDetailView(generics.RetrieveAPIView):
    queryset = Vendor.objects.select_related('user').all()
    serializer_class = AdminVendorListSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
