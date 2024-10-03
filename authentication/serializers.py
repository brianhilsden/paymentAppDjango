from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email is None or password is None:
            raise serializers.ValidationError('Must include "email" and "password".')

        try:
            user = CustomUser.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        self.user = user
        return super().validate(attrs)



      

            

class UserSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','phone_number','role']
