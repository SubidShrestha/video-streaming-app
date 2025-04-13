from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class AbstractTimestampMixin(models.Model):
    """Abstract Timestamp Mixin Model to log model instance creation and modification timestamps"""
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_at', 'id']
        get_latest_by = 'created_at'

class AbstractUserstampMixin(models.Model):
    """Abstract Userstamp Mixin Model to log model instance creator and modifier"""
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='%(class)s_created', verbose_name=_('created_by'), null=True, blank=True)
    updated_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='%(class)s_updated', verbose_name=_('updated_by'), null=True, blank=True)

    class Meta:
        abstract = True

class AbstractStatusMixin(models.Model):
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    last_deactivated_at = models.DateTimeField(verbose_name=_('last deactivated at'), null=True, blank=True)
    last_reactivated_at = models.DateTimeField(verbose_name=_('last reactivated at'), null=True, blank=True)

    class Meta:
        abstract = True
