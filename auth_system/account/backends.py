from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackendAllowInactive(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        identifier = email or username
        if identifier is None or password is None:
            return None
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None