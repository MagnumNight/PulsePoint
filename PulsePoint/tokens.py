from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
<<<<<<< HEAD
account_activation_token = TokenGenerator()
=======
account_activation_token = TokenGenerator()
>>>>>>> fa42bb77b86d5fd77c2128ec4cbee5e48319839d
