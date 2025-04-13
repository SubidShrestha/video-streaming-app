from typing import Any
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.views.decorators.debug import sensitive_variables
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import AuthUserManager
from shared.mixins.model_mixins import AbstractTimestampMixin, AbstractStatusMixin

signer = TimestampSigner()

class User(AbstractBaseUser, PermissionsMixin, AbstractTimestampMixin, AbstractStatusMixin):
    """Custom User Model for authentication"""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name = _('username'),
        max_length=26,
        unique=True,
        help_text=_(
            'Required. 26 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('The username is already taken.'),
        },
    )
    first_name = models.CharField(verbose_name=_('first name'), max_length=150)
    last_name = models.CharField(verbose_name=_('last name'), max_length=150)
    profile_image = models.ImageField(verbose_name=_('profile image'), null=True, blank=True)
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with this email address already exists.')
        }
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = AuthUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=('username',), name='idx_username'),
            models.Index(fields=('email',), name='idx_email'),
        ]

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self) -> str:
        return f"User <{self.username}>"

    @property
    def full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def reset_token(self) -> str:
        """Generates url friendly reset password token"""
        raw = f"{self.pk}:{self.username}"
        signed = signer.sign(raw)
        return urlsafe_b64encode(signed.encode()).decode()
    
    @property
    def reset_password_link(self) -> str:
        reset_token = self.reset_token
        reset_url: str = settings.RESET_PASSWORD_URL
        reset_url.rstrip('/')
        return f"{reset_url}/?token={reset_token}"
    
    @staticmethod
    @sensitive_variables('token')
    def from_token(token: str):
        """
        Returns a User instance from token or raises.
        """
        try:
            decoded = urlsafe_b64decode(token.encode()).decode()
            raw = signer.unsign(decoded, max_age=settings.RESET_PASSWORD_TIMEOUT)
            user_id_str, username = raw.split(":", 1)

            return User.objects.get(id=int(user_id_str), username=username)
            
        except SignatureExpired:
            raise ValueError(_('The reset link has already expired.'))
        except (BadSignature, User.DoesNotExist, Exception):
            raise ValueError(_('The reset link is invalid.'))
