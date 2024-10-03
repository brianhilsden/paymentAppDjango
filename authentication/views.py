# Create your views here.

from rest_framework import status,permissions

from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import CustomUser
from buyer.models import Buyer
from seller.models import Seller
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        role = request.data.get('role')

        if not all([username, password, email, phone_number, role]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(email=email).exists():
                    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username,password=password,email=email)

        if role == "Buyer":
            buyer = Buyer.objects.create_user(user=user, phone_number=phone_number, role=role)
            buyer.save()
            
        
        elif role == "Seller":
            seller = Seller.objects.create_user(user=user, phone_number=phone_number, role=role)
            seller.save()
           
        
        else:
            return Response({"error":"Invalid role specified"},status=status.HTTP_400_BAD_REQUEST)
        
        token_serializer = CustomTokenObtainPairSerializer(data={"username":username,'email':email,'password':password})

        if token_serializer.is_valid():
            tokens = token_serializer.validated_data

            user_data = {
                  "username":user.username,
                  "email":user.email,
                  "phone_number":phone_number,
                  "role":role

            }

            return Response({"tokens":tokens,"user":user_data},status=status.HTTP_201_CREATED)
        
        return Response({"error": "Unable to generate tokens"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CustomTokenObtainPairView(TokenObtainPairView):
      serializer_class = CustomTokenObtainPairSerializer    

      def post(self,request,*args,**kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data

            user = serializer.user

            user_data = {
                 
                  'email':user.email,
            }

            try:
                buyer = Buyer.objects.get(user=user)
                user_data["phone_number"] = buyer.phone_number
                user_data["role"] = "Buyer"
            except Buyer.DoesNotExist:
                    try:
                        seller = Seller.objects.get(user=user)
                        user_data["phone_number"] = seller.phone_number
                        user_data['role'] = "Seller"
                    except Seller.DoesNotExist:
                        user_data["phone_number"] = None
                        user_data["role"] = None

            return Response({"tokens":tokens,"user":user_data}, status=status.HTTP_200_OK)




class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure that the user is authenticated

    def get(self, request, *args, **kwargs):
        user = request.user 

        phone_number = None
        role = None

        try:
             buyer = Buyer.objects.get(user=user)
             phone_number = buyer.phone_number
             role = buyer.role
        
        except Buyer.DoesNotExist:
             pass
        try:
             seller = Seller.objects.get(user=user)
             phone_number = seller.phone_number
             role = seller.role
        
        except Seller.DoesNotExist:
             pass
        serializer = UserSerializer(user) 
        response_data = serializer.data
        response_data['phone_number'] = phone_number
        response_data['role'] = role
        return Response(response_data, status=status.HTTP_200_OK) 


