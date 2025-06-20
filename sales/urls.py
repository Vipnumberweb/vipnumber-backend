from django.urls import path
from .views import *

urlpatterns = [
    path('sales/all/', AllSalesView.as_view()),
    path('sales/pending/', PendingOrdersView.as_view()),
    path('sales/vendor/', SalesByVendors.as_view()),
    path("sales/filter/", FilterSalesView.as_view()),
    path('sales/send/upc/', SendSMSView.as_view()),
    path('sales/vendor/<int:id>/', SalesByVendorView.as_view()),
    path('sales/<uuid:pk>/update/', UpdateOrderDetails.as_view()),
    path('purchases/customer/', PurchasesByCustomers.as_view()),
    path('purchase/number/', BuyNumberView.as_view()),
]