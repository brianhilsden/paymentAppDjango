from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id","message", "product_name", "quantity", "total_price", "date", "status", "buyer", "seller", "purchase_link", "token"]