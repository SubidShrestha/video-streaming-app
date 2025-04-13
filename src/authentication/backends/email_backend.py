from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        """Authenticate user with email"""
        if not email:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        
        if email is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_email_field(email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user