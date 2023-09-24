from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """Можно добавлять только сслыки на youtube"""
        video_url = value.get('video_url')
        if video_url is not None and 'www.youtube' not in video_url:
            raise ValidationError('Допустимы ссылки только на youtube')
