
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResponseSerializer, ShortFormSerializer, LongFormSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .functions import *

@swagger_auto_schema(methods=['post'], request_body=ShortFormSerializer)
@api_view(['POST'])
def link_shorten(request):
    response = {}
    url = get_link(request.data['longUrl'])
    if CustomUrl.objects.filter(longUrl__contains = url).exists():        
        urlObject = CustomUrl.objects.filter(longUrl__contains = url).first()
        url_link = urlObject.get_shortened_url()
    else:
        urlObject = CustomUrl(longUrl = url)
        url_link = urlObject.get_shortened_url()
        urlObject.shortUrl = url_link
        urlObject.save()

    domain = request.META['HTTP_HOST']
    url_link = domain+'/'+url_link+'/'
    response['data'] = url_link
    # GetLinkShortSerializer()
    return Response(response, status= 200)

@swagger_auto_schema(methods=['post'], request_body=LongFormSerializer)
@api_view(['POST'])
def link_expander(request):
    response = {}
    url_link = request.data['shortUrl']
    url_link = get_link(url_link)
    domain = request.META['HTTP_HOST']
    url_link = url_link.strip(domain).strip('/')
    response['data'] = ResponseSerializer(url_link, many=False).data
    # GetLinkShortSerializer()
    return Response(response, status= 200)
