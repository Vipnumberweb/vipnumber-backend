from django.urls import path
from .views import PaymentInitiateView, PaymentCallbackView, PaymentStatusView

urlpatterns = [
    path('initiate/<uuid:sale_id>/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('callback/<uuid:payment_id>/', PaymentCallbackView.as_view(), name='payment-callback'),
    path('status/<uuid:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),
]