from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If this is a Django ValidationError, format it for the API
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            data = {'error': exc.message_dict}
        else:
            data = {'error': exc.messages if hasattr(exc, 'messages') else str(exc)}
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return response