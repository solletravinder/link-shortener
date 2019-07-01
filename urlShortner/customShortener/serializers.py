# serializers.py

from rest_framework import serializers
from .models import CustomUrl


class GetLinkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUrl
        fields = '__all__'

class FormSerializer(serializers.Serializer):
    longUrl = serializers.CharField(style={'input_type': 'text'})
    # def __init__(self, *args, **kwargs):

        
class ResponseSerializer(serializers.Serializer):
    link_data = serializers.SerializerMethodField('get_link')
    def get_link(self, obj):
        return GetLinkShortSerializer(CustomUrl.objects.filter(longUrl = obj.longUrl),many=True).data