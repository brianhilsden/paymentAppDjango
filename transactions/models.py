from django.db import models

# Create your models here.

class Transaction(models.Model):

    message = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255,default="Pending")
    buyer = models.ForeignKey('buyer.Buyer',on_delete=models.CASCADE, related_name="transactions",blank=True,null=True)
    seller = models.ForeignKey('seller.Seller',on_delete=models.CASCADE, related_name="transactions")
    purchase_link = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
  

    def __str__(self):
        return self.product_name
    