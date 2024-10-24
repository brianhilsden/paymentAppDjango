# main urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seller/', include('seller.urls')),
    path('buyer/', include('buyer.urls')),
    path('transactions/', include('transactions.urls')),
    path('', include("authentication.urls")),
    path('api/docs/', include('paymentApp.swagger_urls')),  
]
