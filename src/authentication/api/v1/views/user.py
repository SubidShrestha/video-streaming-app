from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from ..serializers.user import UserSerializer, LogoutSerializer, ChangePasswordSerializer
from shared.mixins.view_mixins import CustomCreateAPIView

@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='retrieve-profile',
        summary='API to view user profile'
    ),
    name='get'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='update-profile',
        summary='API to update user profile'
    ),
    name='put'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='put'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='partial-update-profile',
        summary='API to partially update user profile'
    ),
    name='patch'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='patch'
)
class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return UserSerializer.Meta.model.objects.none()
    
@method_decorator(
    decorator=sensitive_post_parameters('refresh'),
    name='dispatch'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='logout-user',
        summary='API to logout user'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class LogoutView(CustomCreateAPIView):
    queryset = None
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(
    decorator=sensitive_post_parameters('old_password', 'new_password1', 'new_password2'),
    name='dispatch'
)
@method_decorator(
    decorator=extend_schema(
        tags=['User'],
        operation_id='change-password',
        summary='API to change the password for authenticated user'
    ),
    name='post'
)
@method_decorator(
    decorator=transaction.atomic(),
    name='post'
)
class ChangePasswordView(CustomCreateAPIView):
    queryset = None
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
