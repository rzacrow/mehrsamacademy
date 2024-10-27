from django.db import models
from accounts.models import User

# Create your models here.

class Order(models.Model):
    DEGREE_CHOICES = (
        ("D", "دیپلم"),
        ("A", "کاردانی"),
        ("B", "کارشناسی"),
        ("M", "ارشد"),
        ("P", "دکترا"),
    )

    ORDER_STATUS = (
        ("A", "در انتظار بررسی"),
        ("B", "در انتظار پرداخت"),
        ("C", "پرداخت شده، در حال پردازش"),
        ("D", "تحویل داده شده"),
    )
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default="A")
    title = models.CharField(max_length=555, verbose_name="عنوان")
    caption = models.CharField(max_length=2000, blank=True, null=True, verbose_name="توضیحات تکمیلی")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت سفارش")
    


    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارشات'
    
    def __str__(self) -> str:
        try: 
            return f"{self.full_name}"
        except:
            return f"{self.ordered_at}"
