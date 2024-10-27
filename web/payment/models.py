from django.db import models
from accounts.models import User
from order.models import Order
# Create your models here.

class Invoice(models.Model):
    INVOICE_STATUS = (
        ('Active', 'فعال'),
        ('Paid', 'پرداخت شده'),
        ('Expired', 'منقضی شده'),
        ('Failed', 'پرداخت ناموفق'),
    )

    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    authority = models.CharField(max_length=36, blank=True)
    url = models.CharField(max_length=555)
    
    def __str__(self) -> str:
        return f"{self.order.user.first_name} {self.order.user.last_name}"
    
    class Meta:
        verbose_name = 'پرداخت ها'
        verbose_name_plural = 'پرداخت ها'