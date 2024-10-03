
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.views import APIView
from .models import Transaction
from seller.models import Seller
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
import uuid

# Create your views here.

class TransactionsListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    
    def get(self,request,format=None):
        if request.user.is_anonymous:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        if request.user.is_anonymous:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        message = request.data.get("message")
        product_name = request.data.get("product_name")
        quantity = request.data.get("quantity")
        total_price = request.data.get("total_price")
        user = request.user
        
        try:
            seller = Seller.objects.get(user=user)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)
        token = str(uuid.uuid4()) 
        purchase_link = f"http://192.168.100.4:3000/{token}"

        transaction_data = {
            'message': message,
            'product_name': product_name,
            'quantity': quantity,
            'total_price': total_price,
            'seller': seller.id,
            'token': token,  
            'purchase_link': purchase_link,
        }
      
        serializer = TransactionSerializer(data=transaction_data)

        if serializer.is_valid():
           
            transaction = serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TransactionRetrieveUpdateDestroy(APIView):
    def get(self,request,pk,format=None):
        transaction = get_object_or_404(Transaction,pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk,format=None):
        transaction = get_object_or_404(Transaction,pk=pk)
        serializer = TransactionSerializer(transaction,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        transaction = get_object_or_404(Transaction,pk=pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionByToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, token, format=None):
        try:
            transaction = get_object_or_404(Transaction, token=token)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found or token is incorrect'}, status=status.HTTP_404_NOT_FOUND)


        

        

