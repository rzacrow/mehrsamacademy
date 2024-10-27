from django.db import models
from django.contrib.auth.models import Group, Permission, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number must be set")
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def normalize_phone(self, phone):
        return phone.strip().replace(" ", "")

class User(AbstractBaseUser, PermissionsMixin):
    DEGREE_CHOICES = (
        ("D", "دیپلم"),
        ("A", "کاردانی"),
        ("B", "کارشناسی"),
        ("M", "ارشد"),
        ("P", "دکترا"),
    )

    phone = models.CharField(max_length=11, verbose_name="شماره تلفن", unique=True)
    image = models.ImageField(upload_to="accounts/UserProfile/", blank=True, null=True, verbose_name="تصویر پروفایل")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    field = models.CharField(blank=True, null=True, verbose_name="رشته تحصیلی")
    degree = models.CharField(max_length=1, choices=DEGREE_CHOICES, blank=True, null=True, verbose_name="مقطع تحصیلی")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone' 

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Custom related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Custom related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )


    class Meta:
        verbose_name = 'کاربران'
        verbose_name_plural = 'کاربران'
    
    def __str__(self) -> str:
        try: 
            return f"{self.phone}"
        except:
            return self 



from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Token for {self.user.phone}'

    def is_valid(self):
        return (timezone.now() - self.created).seconds < 86400  # 1 day
