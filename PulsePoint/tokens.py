from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


# Class: TokenGenerator - Django token generator for account activation
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

# Class: PasswordResetTokenGenerator - Django token generator for password reset
class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.password)
        )


password_reset_token = PasswordResetTokenGenerator()
