from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeListSerializer

class EmployeeListView(generics.ListAPIView):
    """
    View for listing all employees with limited information
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No employees found"},
                status=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EmployeeDetailView(generics.RetrieveAPIView):
    """
    View for retrieving detailed information about a specific employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing employee operations.
    Provides CRUD operations and additional actions for employee management.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                self.get_serializer(employee).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """
        Upload or update a specific document for an employee.
        Requires document_type and file in request data.
        """
        employee = self.get_object()
        document_type = request.data.get('document_type')
        if document_type not in [field.name for field in Employee._meta.fields if isinstance(field, models.FileField)]:
            return Response(
                {'error': 'Invalid document type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        setattr(employee, document_type, request.FILES['file'])
        employee.save()

        return Response(
            {'message': f'{document_type} uploaded successfully'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        Get a list of all documents associated with an employee.
        Returns document types and their URLs if available.
        """
        employee = self.get_object()
        documents = {}
        for field in Employee._meta.fields:
            if isinstance(field, models.FileField):
                file_field = getattr(employee, field.name)
                if file_field:
                    documents[field.name] = request.build_absolute_uri(file_field.url)
                else:
                    documents[field.name] = None

        return Response(documents)

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to handle deletion of related objects
        """
        instance = self.get_object()
        # Delete related objects first
        if instance.permanent_address:
            instance.permanent_address.delete()
        if instance.communication_address:
            instance.communication_address.delete()
        if instance.bank_account:
            instance.bank_account.delete()
        
        return super().destroy(request, *args, **kwargs)
