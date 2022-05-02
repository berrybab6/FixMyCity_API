from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

USER = get_user_model()


class AuthentificationBackend(ModelBackend):
    """
    Define a new authentification backend for auth with username/password or email/password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(USER.EMAIL_FIELD)

        case_insensitive_email_field = '{}__iexact'.format(USER.EMAIL_FIELD)
        users = USER._default_manager.filter(
            Q(**{case_insensitive_email_field: email}) | Q(email__iexact=email))

        # Test whether any matched user has the provided password:
        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        if not users:
            
            USER().set_password(password)