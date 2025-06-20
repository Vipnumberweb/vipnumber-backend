from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import permissions, status, generics
from .serializers import SalesSerializer, CustomerPurchasesSerializer, VendorSerializer, TotalSalesSerializer
from .models import *
import math
import json
import requests

class AllSalesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        sales = Sales.objects.all()
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PendingOrdersView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Or customize as needed

    def get(self, request):
        pending_sales = Sales.objects.filter()

        serializer = SalesSerializer(pending_sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SalesByVendorView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SalesSerializer

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        sales = Sales.objects.filter(vendors=vendor).distinct()
        serializer = SalesSerializer(sales, many=True)

        vendor_data = VendorSerializer(vendor).data

        return Response({
            "vendor": vendor_data,
            "sales": serializer.data
        }, status=status.HTTP_200_OK)

class SalesByVendors(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SalesSerializer


    def get(self, request):
        try:
            vendor = request.user.vendor_profile
        except Vendor.DoesNotExist:
            return Response({"error": "User is not associated with any vendor profile."}, status=403)

        sales = Sales.objects.filter(vendor=vendor)
        serializer = self.serializer_class(sales, many=True)

        return Response(serializer.data, status=200)

class PurchasesByCustomers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerPurchasesSerializer

    def get(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer is not associated with any vendor profile."}, status=403)

        purchases = Sales.objects.filter(customer=customer)
        serializer = self.serializer_class(purchases, many=True)

        return Response(serializer.data, status=200)


class UpdateOrderDetails(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = get_object_or_404(Sales, pk=order_id)

        # Extract data from request
        agent_name = request.data.get('agent_name')
        agent_order_type = request.data.get('agent_order_type')
        order_status = request.data.get('order_status')
        upc_code = request.data.get('upc_code')  # ✅ Fixed

        # Update fields if provided
        if agent_name is not None:
            order.agent_name = agent_name
        if agent_order_type is not None:
            order.agent_order_type = agent_order_type
        if order_status is not None:
            order.order_status = order_status
        if upc_code is not None:
            order.upc_code = upc_code

        order.save()

        return Response({
            "message": "Order updated successfully.",
            "data": SalesSerializer(order).data
        }, status=status.HTTP_200_OK)


class BuyNumberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        number_ids = request.data.get('number_ids')  # Expect a list of number IDs

        if not number_ids or not isinstance(number_ids, list):
            return Response({"error": "A list of number IDs is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all numbers and validate
        numbers = Number.objects.filter(id__in=number_ids)
        if len(numbers) != len(number_ids):
            # Identify missing IDs for a more helpful error message
            existing_ids = {str(n.id) for n in numbers}
            missing_ids = [n_id for n_id in number_ids if str(n_id) not in existing_ids]
            return Response(
                {"error": f"One or more number IDs are invalid: {', '.join(missing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if any number is already sold
        sold_numbers = numbers.filter(is_sold=True)
        if sold_numbers.exists():
            return Response(
                {"error": f"Numbers {', '.join(n.entry for n in sold_numbers)} are already sold"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check customer profile
        try:
            # Assuming request.user has a one-to-one or reverse foreign key to Customer
            # If your User model has a direct customer field, use that.
            # Otherwise, ensure customer_profile is a valid reverse relation.
            customer = request.user.customer_profile # Or request.user.customer if directly linked
        except AttributeError: # Catch specific attribute error if customer_profile doesn't exist
            return Response({"error": "User is not associated with any customer profile"}, status=status.HTTP_403_FORBIDDEN)
        except Customer.DoesNotExist: # If customer_profile points to a non-existent customer
            return Response({"error": "Customer profile not found for this user"}, status=status.HTTP_404_NOT_FOUND)


        # --- Start of Changes for Financial Calculations ---

        # Calculate total prices based on Number model's price and purchase_price
        order_rate = 0.0      # Sum of Number.price (selling price)
        vendor_rate = 0.0     # Sum of Number.purchase_price (cost from vendor)

        # Collect all unique vendors involved in this sale
        all_vendors = set()

        for number in numbers:
            # Calculate discounted price for each number (if applicable)
            # Make sure number.price and number.discount are numeric
            num_price = float(number.price)
            num_purchase_price = float(number.purchase_price)
            num_discount = float(number.discount)

            # Apply discount to the selling price
            # Your current logic for discounted_price seems to be correct for individual numbers
            # However, you might want to consider if the final_price logic should be moved to the Sales model's save method
            # For now, let's calculate totals here as per your original structure

            # This is the price customer pays for this specific number (after discount)
            effective_selling_price_for_number = num_price - (num_price * (num_discount / 100))

            order_rate += effective_selling_price_for_number
            vendor_rate += num_purchase_price # Vendor rate is just the purchase price for us

            all_vendors.add(number.vendor) # Collect associated vendors

        # Define GST rate (make sure this is consistent, e.g., from settings)
        # Using a hardcoded value for demonstration; consider fetching it from a configuration.
        GST_RATE = 0.18 # 18% GST

        # Calculate totals excluding and including GST
        total_excl_gst = order_rate
        total_incl_gst = total_excl_gst * (1 + GST_RATE)


        # Create the sale object
        # Note: sales_id will be auto-generated in the Sales model's save() method
        # Also, order_rate, vendor_rate, total_excl_gst, total_incl_gst, and final_price
        # will be set by the Sales model's save() method after its initial creation
        # IF you designed calculate_prices() and called it in save().
        # So you could just pass final_price initially, and let the model populate others.
        # However, to be explicit, we'll pass them directly.
        sale = Sales.objects.create(
            customer=customer,
            order_rate=order_rate,         # New field
            vendor_rate=vendor_rate,       # New field
            total_excl_gst=total_excl_gst, # New field
            total_incl_gst=total_incl_gst, # New field
            final_price=total_incl_gst,    # Align final_price with total_incl_gst
            payment_status='pending',      # New field, initial state
            order_status='new',            # New field, initial state as per client's New status
        )

        # Add numbers and vendors to the ManyToMany fields
        sale.numbers.add(*numbers)
        sale.vendors.add(*all_vendors) # Use the collected set of vendors

        # Mark numbers as sold and update their status (if applicable)
        # Assuming you want to update the 'status' field in the Number model
        # You should also update 'is_sold' to True.
        # Make sure NumberStatus.SOLD is defined in your NumberStatus choices
        # for number in numbers:
        #     number.is_sold = True
        #     # Optional: update numberStatus to a 'Sold' equivalent if you have one
        #     # if hasattr(NumberStatus, 'SOLD'): # Check if SOLD choice exists
        #     #     number.numberStatus = NumberStatus.SOLD
        #     number.save(update_fields=['is_sold']) # Save efficiently

        # --- End of Changes ---

        # Assuming SalesSerializer is updated to include all new fields
        serializer = SalesSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SendSMSView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        number = request.data.get('number')
        message = request.data.get('message')
        sales_id = request.data.get('sales_id')  # Pass sale to update status (if desired)

        if not number or not message:
            return Response({"error": "Number and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = send_sms(number, message)

        if response.get('status') == 'success':
            if sales_id:
                try:
                    sale = Sales.objects.get(id=sales_id)
                    sale.order_status = "completed"  # updated in memory only, not saved
                    # Don't save, so it can't be queried later
                except Sales.DoesNotExist:
                    pass  # ignore if sale not found

            return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_sms(number, message):
    # Placeholder function for sending SMS
    # In a real application, you would integrate with an SMS gateway here
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        'route': 'q',
        'message': message,
        'language': 'english',
        'flash': 0,
        'numbers': number
    }

    headers = {
        'authorization': "Y6BlofkwFpvdDKytqO1PMjx0GREZNcT5VUrbg4uCHmz38LnsW7i451ajDqOxEbtAMRgPGpZuLNfoSQVF",
        'Content-Type': "application/json",
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()

class FilterSalesView(APIView):
    def get(self, request):
        vendor = request.query_params.get("vendor")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        pattern = request.query_params.get("pattern")
        category = request.query_params.get("category")

        queryset = Sales.objects.all()

        if vendor:
            queryset = queryset.filter(vendor__name__icontains=vendor)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if pattern:
            queryset = queryset.filter(product__name__icontains=pattern)

        if category:
            queryset = queryset.filter(product__category__name__icontains=category)

        serializer = TotalSalesSerializer(queryset, many=True)
        return Response(serializer.data)
