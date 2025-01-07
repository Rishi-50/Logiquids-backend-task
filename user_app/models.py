from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import random
import string

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, mobile_number, city, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile_number=mobile_number, city=city)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, mobile_number, city, password=None):
        user = self.create_user(email, name, mobile_number, city, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# User model with referral code and relation to referred users
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number', 'city', 'password']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.referral_code:  # Only generate if not set
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)

    def generate_unique_referral_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not User.objects.filter(referral_code=code).exists():  # Ensure uniqueness
                return code

    def __str__(self):
        return self.email
