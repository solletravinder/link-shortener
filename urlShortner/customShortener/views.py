from django.shortcuts import render
from .models import CustomUrl
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import FormSerializer, ResponseSerializer
import json
import re
from .functions import *
REGEX_VALUE = """(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
# Create your views here.
def expand(request, url):
    if len(url) == 7:
        if CustomUrl.objects.filter(shortUrl = url).exists():
            urlObject = CustomUrl.objects.get(shortUrl = url)
            return HttpResponseRedirect(urlObject.longUrl)
            # return HttpResponseRedirect("https://www.dropbox.com")
        else:
            return render(request, '404_notfound.html', {})
    else:
        return render(request, '404_notfound.html', {})

def short(request):
    response = {}
    title = "Link Shortener Service"
    context = {
        'title': title,
        'branding_name': "Link Shortener"
    }
    if request.method=='GET':
        return render(request, 'link_shortener.html', context)

    if request.POST['long_url_link']:
        url = get_link(request.POST['long_url_link'])
        if url:
            if CustomUrl.objects.filter(longUrl__contains = url).exists():        
                urlObject = CustomUrl.objects.filter(longUrl__contains = url).first()
                url_link = urlObject.getShortenedURL()
            else:
                urlObject = CustomUrl(longUrl = url)
                url_link = urlObject.getShortenedURL()
                urlObject.shortUrl = url_link
                urlObject.save()
            # print(request.method)
            domain = request.META['HTTP_HOST']
            print(domain)
            url_link = domain+'/'+url_link+'/'
            response = {
                'long_url_link':request.POST['long_url_link'],
                'short_url': url_link,
                'title': title,
                'branding_name': "Link Shortener"
            }
        else:
            context = {
                'messages': 'URL is not valid',
            }
            return render(request, 'link_shortener.html', context) 
    else:
        return render(request, 'link_shortener.html', context)
    return render(request, 'link_shortener.html', response)


from rest_framework.decorators import api_view, permission_classes, renderer_classes, detail_route, list_route

# from rest_framework.permissions import AllowAny

# from rest_framework.schemas import SchemaGenerator

from rest_framework.response import Response

# from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet



# from rest_framework.filters import BaseFilterBackend
# import coreapi

# class SimpleFilterBackend(BaseFilterBackend):
#     def get_schema_fields(self, view):
#         return [coreapi.Field(
#             name='url',
#             location='query',
#             required=True,
#             type='string',
#             description='Type the Link here'
#         )]
#     def filter_queryset(self, request, queryset, view):
#         try:
#             n = request.query_params['url']
#             if queryset.filter(longUrl=n).exists():
#                 queryset = queryset.filter(longUrl=n)
#             elif queryset.filter(shortUrl=n).exists():
#                 queryset = queryset.filter(shortUrl=n)
#         except KeyError:
#             # no query parameters
#             pass
#         return queryset
from drf_yasg.utils import swagger_auto_schema

# class LinkShortenerAPIView(ViewSet):
#     queryset = CustomUrl.objects.all()    
#     serializer_class = FormSerializer
#     filter_backends = (SimpleFilterBackend,)
@swagger_auto_schema(methods=['post'], request_body=FormSerializer)
@api_view(['POST'])
def link_shorten(request):
    response = {}
    response['data'] = ResponseSerializer(request.data, many=True).data
    # GetLinkShortSerializer()
    return Response(response, status= 200)

@swagger_auto_schema(methods=['post'], request_body=FormSerializer)
@api_view(['POST'])
def link_expander(request):
    response = {}
    response['data'] = ResponseSerializer(request.data, many=True).data
    # GetLinkShortSerializer()
    return Response(response, status= 200)