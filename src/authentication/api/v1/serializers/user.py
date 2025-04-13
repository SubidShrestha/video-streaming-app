from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_image'
        ]
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'email': {
                'read_only': True
            }
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
            return {'message': _('Successfully logged out')}
        except TokenError:
            raise serializers.ValidationError(_('Token is invalid or already expired.'))
    
    def to_representation(self, instance):
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, old_password) -> None:
        if not self.user.check_password(old_password):
            raise serializers.ValidationError(_('The old password do not match'))
        
    def validate_new_passwords(self, new_password1, new_password2) -> None:
        if new_password1 != new_password2:
            raise serializers.ValidationError(_('The new passwords do not match'))

    def validate(self, attrs):

        self.user = self.context.get('request', {}).get('user', None)

        attrs = super().validate(attrs)
        old_password = attrs.get('old_password')
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        self.validate_old_password(old_password)
        self.validate_new_passwords(new_password1, new_password2)

        return attrs

    def create(self, validated_data):
        password = validated_data['new_password1']
        self.user.set_password(password)
        self.user.save(update_fields = ['password'])
        return {'message': _('The password has been changed successfully.')}

    def to_representation(self, instance):
        return instance