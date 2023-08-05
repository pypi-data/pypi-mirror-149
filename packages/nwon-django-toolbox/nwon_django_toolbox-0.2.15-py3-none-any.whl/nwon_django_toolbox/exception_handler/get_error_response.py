from http import HTTPStatus
from typing import List, Union

from nwon_baseline.typings import AnyDict

from nwon_django_toolbox.nwon_django_settings import NWONDjangoSettings
from nwon_django_toolbox.typings.error_response import ErrorResponse


def get_error_response(
    details: Union[AnyDict, List, None] = None,
    status_code: int = 200,
) -> AnyDict:
    # Using the description's of the HTTPStatus class as error message.
    http_code_to_message = {v.value: v.description for v in HTTPStatus}

    return ErrorResponse(
        message=http_code_to_message[status_code],
        details=details,
        status_code=status_code,
        api_docs=NWONDjangoSettings.api_docs_url,
    ).dict()
