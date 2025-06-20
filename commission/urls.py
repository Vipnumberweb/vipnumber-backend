from django.urls import path
from .views import *

urlpatterns = [
    path('', CommissionByCategoriesView.as_view()),
    path('price/', CommissionByPriceRangeView.as_view(), name='commission-list-create'),
    path('price/<uuid:id>/', CommissionByPriceRangeDetailView.as_view(), name='commission-detail'),
    path('price/<uuid:id>/update/', CommissionByPriceRangeUpdateView.as_view(), name='commission-update'),
    path('price/<uuid:id>/delete/', CommissionByPriceRangeDeleteView.as_view(), name='commission-delete'),
    path('update/', UpdateCommissionView.as_view()),
    path('settings/', CommissionSettingsView.as_view()),
    path('new/<int:id>/', NewNumbersCommissionView.as_view()),
    path('exist/<int:id>/', ExistingNumberCommissionView.as_view())
]