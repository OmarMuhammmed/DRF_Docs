# DRF_Docs
docs for Django rest framework Api

# Requests 
## parsing :-
Deal with incoming data in the request object to convert from (json, xml,etc) to python objects 

Each view in DRF can determine parser classes if not determined then it will use the `DEFAULT_PARSER_CLASSES`

If clint sent a not valid data ex (JSON with errors ) request then DRF return `ParseError` and `Bad Request 400`

If clint sent not suportted data ex (XML) request then DRF return `Unsupported Media Type` and `415`

### request parsing :-
- request.data -> returns the parsed content of the request body
- request.query_params -> returns the parsed content of the query string parameters better than request.GET because it handles multiple values for the same key and works for all HTTP methods

## Authentication :-
- request.user -> returns the user associated with the current request equal instance of `django.contrib.auth.models.User` if not authenticated then `AnonymousUser` instance
- request.auth -> returns the authentication instance associated with the request if any
and it's a tuple of (user, auth) if not authenticated and Token invaild then `None` (related to policies authentication)
- DRF return `WrappedAttributeError` if probkem in the authentication process not request erorr

## Browser enhancements :-
REST framework supports a few browser enhancements such as browser-based PUT, PATCH and DELETE forms
- `request.method` returns the uppercased string representation of the request's HTTP method.
- `request.content_type` returns the content type of the request payload (JSON, XML, form data, etc..)
- `request.body` returns the raw request body as a byte string 

# Responses
- Response in DRF: Provides an easy interface for responses in APIs and supports more than one format.
- `TemplateResponse`: Delays the response until the client requests it.
- `APIView` or `@api_view`: Provides content negotiation automatically (can control format type (XML, JSON )).
- `HttpResponse`: Use it for simple responses without content negotiation.
- `Response`(data, status=200(bydafult), template_name=None, headers=None, content_type=None)

# Views 
- `APIView` class: The base class for all views in DRF. It provides the core functionality of views in DRF.
- `@api_view` decorator: Wraps a function-based view to create an API view.
- `APIview`FUll Control :- 
```from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, renderers, parsers, throttling

class CustomAPIView(APIView):
    """
    مثال على استخدام إعدادات API المختلفة في APIView.
    """

    # تحديد نوع الاستجابة (هنا بنخليه يدعم JSON و HTML)
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    # تحديد أنواع البيانات اللي الطلب ممكن يقبلها (JSON و Form Data)
    parser_classes = [parsers.JSONParser, parsers.FormParser]

    # تحديد طرق المصادقة (هنا بنستخدم المصادقة بالتوكين)
    authentication_classes = [authentication.TokenAuthentication]

    # تحديد الصلاحيات (هنا لازم المستخدم يكون Admin عشان يدخل)
    permission_classes = [permissions.IsAdminUser]

    # تحديد معدل الطلبات (هنا بنحدده بـ 10 طلبات كل دقيقة) ratelimit 
    throttle_classes = [throttling.UserRateThrottle]

    # تنفيذ الطلب
    def get(self, request, format=None):
        data = {"message": "مرحبًا، هذه استجابة من APIView مع إعدادات مخصصة!"}
        return Response(data, template_name='custom_template.html')
```
## DRF request response lifecycle
Request-> dispath() -> get or post or put or delete -> Authentication (user have a token or not )-> Permission (user have permission or not) -> Throttling (user have a limit or not) -> Parser (parse the request) -> View (handle the request) -> Serializer (validate the data) -> Response (return the response) 

## Rate Limiting
- Rate limiting is a way to control the number of requests that a client can make to an API.
```from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```
- @renderer_classes(...) -> Specifies the response type such as JSON, XML, or HTML
- @parser_classes(...) -> Specifies the data types that the API can accept
- @authentication_classes(...) -> Specifies authentication methods such as Token or Session)
- @permission_classes(...) -> Specifies access permissions
- @schema(...) -> Used to specify how the schema is generated