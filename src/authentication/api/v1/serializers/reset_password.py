from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from ....tasks import send_reset_mail

from rest_framework import serializers

UserModel = get_user_model()

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        try:
            user = UserModel.objects.get_by_email_field(email)
            send_reset_mail.delay(user.pk)
        except UserModel.DoesNotExist:
            pass  
        return {'message': _('If this email is associated with an account, a reset link has been sent.')}

    def to_representation(self, instance):
        return instance
        
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise serializers.ValidationError(_('The passwords do not match.'))

        token_data = UserModel.verify_token(attrs['token'])
        if not token_data.get('success'):
            raise serializers.ValidationError(token_data.get('message'))

        try:
            user = UserModel.objects.get(pk=token_data['user_id'], username=token_data['username'])
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(_('Invalid token or user not found.'))

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        password = validated_data['password1']
        user.set_password(password)
        user.save(update_fields=['password'])
        return {'message': _('Your password has been reset successfully.')}
    
    def to_representation(self, instance):
        return instance