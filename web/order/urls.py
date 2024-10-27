from django.urls import path
from .views import SubmitOrder, OrderChange, OrdersList

urlpatterns = [
    path('submit/', SubmitOrder.as_view(), name="submit-order"),
    path('change/status/', OrderChange.as_view(), name="change-order"),
    path('list/', OrdersList.as_view(), name="orders-list"),
]