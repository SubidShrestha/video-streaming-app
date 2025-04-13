from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers.login import LoginSerializer

@method_decorator(
    decorator=sensitive_post_parameters('password'),
    name='dispatch'
)
@method_decorator(
    extend_schema(
        tags=['User'],
        operation_id='login',
        summary='API to login user'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class LoginView(generics.CreateAPIView):
    """
    API to login user with email or username
    """
    queryset = None
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response