from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Create the schema view with security definitions
schema_view = get_schema_view(
    openapi.Info(
        title="Payment App API",
        default_version='v1',
        description="API documentation for PaymentApp",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="brianhilsden@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define security schemes directly in the schema_view
schema_view.openapi_schema = {
    'components': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
    'security': [
        {'Bearer': []}  # This indicates that Bearer token is required for all operations
    ]
}

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
