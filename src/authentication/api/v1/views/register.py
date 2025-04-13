from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from ..serializers.register import RegisterSerializer

@method_decorator(
    decorator=sensitive_post_parameters('password1', 'password2'),
    name='dispatch'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='register',
        summary='API to register user'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class RegisterView(generics.CreateAPIView):
    """
    API to register user manually with email, username, passwords, etc.
    """
    queryset = RegisterSerializer.Meta.model.objects.all()
    serializer_class = RegisterSerializer