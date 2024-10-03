from django.urls import path
from .views import CustomTokenObtainPairView,signup,UserProfileView

app_name = "authentication"


urlpatterns = [
    path("login/",CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("signup/",signup,name="signup"),
    path('check_session/',UserProfileView.as_view(),name="user")
]
