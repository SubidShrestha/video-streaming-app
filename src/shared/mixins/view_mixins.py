from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status

class DisablePartialUpdateMixin:
    def partial_update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(_('PATCH method is not allowed'))
    
class DisableUpdateMixin:
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(_('PUT method is not allowed'))

class CustomCreateAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response
