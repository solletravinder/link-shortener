# serializers.py

from rest_framework import serializers
from .models import CustomUrl


class GetLinkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUrl
        fields = '__all__'
class FormSerializer(serializers.Serializer):
    # long_url = serializers.CharField()
    link_data = serializers.SerializerMethodField('get_link')
    def __init__(self, *args, **kwargs):
        context = kwargs.pop("context")
        self.long_url = context.get('longUrl')
        super(FormSerializer, self).__init__(*args, **kwargs)
    def get_link(self, obj):
        return GetLinkShortSerializer(CustomUrl.objects.filter(longUrl = self.long_url),many=True).data