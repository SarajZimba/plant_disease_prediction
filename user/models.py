
import uuid
        
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    reset_token = models.CharField(max_length = 1000, default=uuid.uuid4, editable=False)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    objects = CustomerManager()

    def __str__(self):
        return self.username