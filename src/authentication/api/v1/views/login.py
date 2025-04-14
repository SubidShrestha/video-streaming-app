from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from ..serializers.login import LoginSerializer
from shared.mixins.view_mixins import CustomCreateAPIView

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
class LoginView(CustomCreateAPIView):
    """
    API to login user with email or username
    """
    queryset = None
    serializer_class = LoginSerializer