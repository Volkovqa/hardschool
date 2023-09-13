from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video_url')
        if ('www.youtube' not in video_url) and ('https://youtu.be' not in video_url):
            raise ValidationError('Разрешены ссылки только на youtube')
