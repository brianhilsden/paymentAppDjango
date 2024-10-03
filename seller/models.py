from django.db import models

from authentication.models import CustomUser

# Create your models here.

class SellerManager(models.Manager):
    def create_user(self,user,phone_number,role):
        seller = self.create(user=user,phone_number=phone_number,role=role)
        return seller

class Seller(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    
    objects = SellerManager()


    def __str__(self):
        return self.user.username