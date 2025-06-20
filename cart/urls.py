from django.urls import path
from .views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart-list-create'),
    path('<uuid:number_id>/', CartView.as_view(), name='cart-delete'),
]