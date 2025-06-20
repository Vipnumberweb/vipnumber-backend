from django.urls import path
from .views import *

urlpatterns = [
    path('all/', NumberListCreateAPIView.as_view()),
    path('random/', GetRandomDataView.as_view()),
    path('premium/', GetPremiumNumbers.as_view()),
    path('delete/all/', DeleteAllNumbersView.as_view()),
    path('discounted/', GetDiscountedNumbers.as_view()),
    path('filter/', NumberFilterAPIView.as_view()),
    path("by-vendor/", VendorNumbersAPIView.as_view(), name=""),
    path("pattern/<int:id>/", PatternNumbersAPIView.as_view(), name=""),
    path("add/", VendorAddNumbersAPIView.as_view(), name=""),
    path("add/admin/", AdminNumberCreateView.as_view(), name=""),
    path('<uuid:id>/', GetNumber.as_view(), name='get-number'),
    path('<uuid:id>/update/', NumberUpdateAPIView.as_view(), name='number-update'),
    path('<uuid:id>/delete/', NumberDeleteAPIView.as_view(), name='number-delete'),
    path('<uuid:id>/approve/', NumberApprovalView.as_view(), name="number-approve"),
    path('<uuid:id>/reject/', NumberRejectionView.as_view(), name="number-reject"),
    path('pattern/create/', PatternCreateView.as_view(), name="create-pattern"),
    path('patterns/', GetAllPatternsView.as_view(), name="all-patterns"),
    path('patterns/<int:id>/', GetPatternByIdView.as_view(), name="pattern-detail"),
    path('patterns/<int:id>/delete/', PatternDeleteAPIView.as_view(), name="pattern-delete"),
    path('approved/', ApprovedNumbersView.as_view(), name="approved-numbers"),
    path('unapproved/', UnapprovedNumbersView.as_view(), name="unapproved-numbers"),
    path('similar/', SimilarVIPNumbersView.as_view(), name="similar-numbers"),
    path('all/unsold/', UnsoldNumberListView.as_view(), name="all-unsold-numbers"),
    path('mark/admin/', MarkedNumbersByAdmin.as_view())
]