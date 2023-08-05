from django.http import JsonResponse

from nwon_django_toolbox.exception_handler.get_error_response import (
    get_error_response as custom_get_response,
)


class ExceptionMiddleware(object):
    def __init__(self, get_response=custom_get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            response.data = custom_get_response(
                details=response.data,
                status_code=response.status_code,
            )

            return JsonResponse(response, status=response.status_code)

        if response.status_code == 404 and "Page not found" in str(response.content):
            response.data = custom_get_response(
                details=response.data,
                status_code=response.status_code,
            )

            return JsonResponse(response, status=response.status_code)

        return response
