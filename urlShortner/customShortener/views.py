from django.shortcuts import render
from .models import CustomUrl
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import FormSerializer
import json
# Create your views here.
def expand(request, url):
    if len(url) == 7:
        if CustomUrl.objects.filter(shortUrl = url).exists():
            urlObject = CustomUrl.objects.get(shortUrl = url)
            return HttpResponseRedirect("http://"+urlObject.longUrl)
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
        if CustomUrl.objects.filter(longUrl = request.POST['long_url_link']).exists():        
            urlObject = CustomUrl.objects.get(longUrl = request.POST['long_url_link'])
            url_link = urlObject.getShortenedURL()
        else:
            urlObject = CustomUrl(longUrl = request.POST['long_url_link'])
            url_link = urlObject.getShortenedURL()
            urlObject.shortUrl = url_link
            urlObject.save()
        # print(request.method)
        domain = request.META['HTTP_HOST']
        print(domain)
        url_link = domain+'/'+url_link
        response = {
            'long_url_link':request.POST['long_url_link'],
            'short_url': url_link,
            'title': title,
            'branding_name': "Link Shortener"
        }
    else:
        return render(request, 'link_shortener.html', context)
    return render(request, 'link_shortener.html', response)


from rest_framework.decorators import api_view, permission_classes, renderer_classes, detail_route, list_route

from rest_framework.permissions import AllowAny

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from rest_framework.schemas import SchemaGenerator

from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet


@api_view()

@permission_classes((AllowAny, ))

@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])

def schema_view(request):

    generator = SchemaGenerator(title='Link Shortener APIs')

    return Response(generator.get_schema(request=request))

from rest_framework.filters import BaseFilterBackend
import coreapi

class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='url',
            location='query',
            required=True,
            type='string',
            description='Type the Link here'
        )]
    def filter_queryset(self, request, queryset, view):
        try:
            n = request.query_params['url']
            if queryset.filter(longUrl=n).exists():
                queryset = queryset.filter(longUrl=n)
            elif queryset.filter(shortUrl=n).exists():
                queryset = queryset.filter(shortUrl=n)
        except KeyError:
            # no query parameters
            pass
        return queryset


class LinkShortenerAPIView(ViewSet):
    queryset = CustomUrl.objects.all()    
    serializer_class = FormSerializer
    filter_backends = (SimpleFilterBackend,)
    @list_route(methods = ['POST'])
    def link_shorten(self, request):
        response = {}
        response['data'] = FormSerializer(context={"longUrl": request.data['long_url']},many=True).data
        # GetLinkShortSerializer()
        return Response(response, status= 200)
    @list_route(methods = ['POST'])
    def link_expander(self, request):
        response = {}
        response['data'] = FormSerializer(context={"shortUrl": request.data['long_url']},many=True).data
        # GetLinkShortSerializer()
        return Response(response, status= 200)