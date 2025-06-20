from django.urls import path
from .views import CustomerProfileView, CustomerDeactivateView

urlpatterns = [
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('deactivate/', CustomerDeactivateView.as_view(), name='customer-deactivate'),
]