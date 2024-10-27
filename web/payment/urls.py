from django.urls import path
from .views import VerifyPayment, GetAuthority, InvoiceListView



urlpatterns = [
    path('verify/', VerifyPayment.as_view(), name="verify_payment"),
    path('authority/', GetAuthority.as_view(), name="authority"),
    path('InvoiceList/', InvoiceListView.as_view(), name='InvoiceList')
]