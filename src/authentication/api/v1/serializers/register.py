from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ....tasks import send_register_mail

UserModel = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_active',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'null': _('The username field is missing'),
                    'required': _('The username field is missing'),
                    'blank': _('The username field is missing'),
                    'invalid': _('Letters, digits and @/./+/-/_ only.'),
                    'max_length': _('The username must be 26 characters or fewer')
                }
            },
            'email': {
                'error_messages': {
                    'null': _('The email is missing'),
                    'required': _('The email is missing'),
                    'blank': _('The email is missing'),
                    'invalid': _('The given email address is invalid')
                }
            },
            'is_active': {
                'read_only': True
            }
        }
    
    def _validate_password(self, password1, password2):
        if password1 != password2:
            raise serializers.ValidationError(_('The passwords do not match.'))
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        self._validate_password(password1 = password1, password2 = password2)
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        _ = validated_data.pop('password2')
        user = UserModel.objects.create_user(
            **validated_data,
            password=password
        )
        send_register_mail.delay(user.pk)
        return user