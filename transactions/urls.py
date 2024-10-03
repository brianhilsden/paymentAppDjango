
from django.urls import path
from . import views

urlpatterns = [
    path("",views.TransactionsListCreate.as_view(),name="transactions"),
    path("transactionById/<int:pk>",views.TransactionRetrieveUpdateDestroy.as_view(), name="updates"),
    path("transactionByToken/<str:token>",views.TransactionByToken.as_view(),name="transaction_token")
  
]
