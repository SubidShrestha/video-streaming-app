from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers.reset_password import ResetPasswordRequestSerializer, ResetPasswordSerializer

@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='reset-password-request',
        summary='API to request token for resetting password'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class ResetPasswordRequestView(generics.CreateAPIView):
    queryset = None
    serializer_class = ResetPasswordRequestSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

@method_decorator(
    decorator=sensitive_post_parameters('password1', 'password2', 'token'),
    name='dispatch'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='reset-password',
        summary='API to reset user password'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class ResetPasswordView(generics.CreateAPIView):
    queryset = None
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response