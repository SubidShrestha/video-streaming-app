from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from ..serializers.reset_password import ResetPasswordRequestSerializer, ResetPasswordSerializer
from shared.mixins.view_mixins import CustomCreateAPIView

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
class ResetPasswordRequestView(CustomCreateAPIView):
    queryset = None
    serializer_class = ResetPasswordRequestSerializer


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
class ResetPasswordView(CustomCreateAPIView):
    queryset = None
    serializer_class = ResetPasswordSerializer
