from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeListView, EmployeeDetailView

router = DefaultRouter()
router.register(r'manage', EmployeeViewSet)

urlpatterns = [
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('detail/<uuid:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('', include(router.urls)),
]