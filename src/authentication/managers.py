from django.contrib.auth.models import UserManager

class AuthUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, username, email = ..., password = ..., **extra_fields):
        return super().create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)
    
    def get_by_email_field(self, email):
        return self.model._default_manager.get(**{self.model.EMAIL_FIELD: email})
