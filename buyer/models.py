from django.db import models

from authentication.models import CustomUser

# Create your models here.

class BuyerManager(models.Manager):
    def create_user(self,user,phone_number,role):
        buyer = self.create(user=user,phone_number=phone_number,role=role)
        return buyer

class Buyer(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    objects = BuyerManager()

    def __str__(self):
        return self.user.email