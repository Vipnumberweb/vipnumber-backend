from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class VN_User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone = models.CharField(max_length=10, unique=True, )
    phone_verified = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)