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

