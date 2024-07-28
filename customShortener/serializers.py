# serializers.py

from rest_framework import serializers
from .models import CustomUrl


class GetLinkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUrl
        fields = '__all__'

class LongFormSerializer(serializers.Serializer):
    shortUrl = serializers.CharField(style={'input_type': 'text'})
    # def __init__(self, *args, **kwargs):

class ShortFormSerializer(serializers.Serializer):
    longUrl = serializers.CharField(style={'input_type': 'text'})
        
class ResponseSerializer(serializers.Serializer):
    link_data = serializers.SerializerMethodField('get_link')
    def get_link(self, obj):
        return GetLinkShortSerializer(CustomUrl.objects.filter(shortUrl = obj),many=True).data
