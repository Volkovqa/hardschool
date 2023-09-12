from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:

    def __call__(self, value):
        value = value.lower()

        if 'https' in value or '.com' in value:
            if 'youtube.com' not in value and 'youtu.be' not in value:
                raise ValidationError("Разрешены только ссылки на YouTube")
