from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

class DisablePartialUpdateMixin:
    def partial_update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(_('PATCH method is not allowed'))
    
class DisableUpdateMixin:
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(_('PUT method is not allowed'))
