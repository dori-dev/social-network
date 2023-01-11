from django.core.exceptions import ValidationError


class MinimumLengthValidator(object):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                "رمز عبورت خیلی کوتاهه. باید حداقل شامل ۸ کاراکتر باشه.",
                code='password_too_short',
            )

    def get_help_text(self):
        return "رمز عبور باید حداقل شامل ۸ کاراکتر باشد."
