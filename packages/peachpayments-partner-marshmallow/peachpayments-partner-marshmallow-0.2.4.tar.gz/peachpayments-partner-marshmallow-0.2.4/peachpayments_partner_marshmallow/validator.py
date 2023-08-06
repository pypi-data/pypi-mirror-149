"""Provides endpoint field validation."""

from typing import Optional, Type, Union

from peachpayments_partner.error_response import format_error_response
from peachpayments_partner.result_codes import result_codes

from .schemas import (
    CancelRequest,
    CancelResponse,
    DebitRequest,
    DebitResponse,
    Error400Response,
    ErrorResponse,
    RefundRequest,
    RefundResponse,
    StatusResponse,
    WebhookRequest,
    WebhookResponse,
)

ParameterErrorType = dict[str, Optional[str]]
ParameterErrorsType = list[ParameterErrorType]
ErrorResultType = dict[str, Union[ParameterErrorsType, Optional[str]]]
ErrorResponseType = dict[str, Union[str, ErrorResultType]]
ValidateRequestReturnType = dict[
    str,
    Union[
        bool,
        list[str],
        ErrorResponseType,
    ],
]
ValidateResponseReturnType = dict[str, Union[bool, list[str], dict]]
ValidateWebhookRequestType = ValidateResponseReturnType


def _validate_request(schema: Type, data: dict) -> ValidateRequestReturnType:
    """Validate Peach request fields.

    Args:
        schema: Schema class defined in .schemas
        data (dict): request fields as defined in spec

    Returns:
        (dict): validated data and response fields if not valid

    The `response` fields are used to return the error message to the client.

    """
    errors = schema().validate(data)
    if not errors:
        return dict(valid=True)

    result_code = result_codes.INVALID_OR_MISSING_PARAMETER
    return dict(valid=False, errors=errors, response=format_error_response(result_code, errors, data))


def _validate_response(schema: Type, data: dict) -> ValidateResponseReturnType:
    """Validate endpoint response fields.

    Args:
        schema: Schema class defined in .schemas
        data (dict): response fields as defined in spec

    Returns:
        (dict): validated data
    """
    errors = schema().validate(data)
    if not errors:
        return dict(valid=True)

    # PT-572 Workaround for the possible error in the Marshmallow library
    # TODO Investigate and send an issue if needed
    if (
        errors.get("result")
        and isinstance(errors["result"], dict)
        and errors["result"].get("parameterErrors")
        and isinstance(errors["result"]["parameterErrors"], dict)
    ):
        parameter_errors_dict = errors["result"]["parameterErrors"]
        # Convert to list
        parameter_errors: list = []
        for key in parameter_errors_dict:
            parameter_errors.append(parameter_errors_dict[key])

        errors["result"]["parameterErrors"] = parameter_errors

    return dict(valid=False, errors=errors)


def validate_debit_request(data: dict) -> ValidateRequestReturnType:
    """Validate Debit request data.

    Args:
        data (dict): debit request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(DebitRequest, data)


def validate_debit_response(data: dict) -> ValidateResponseReturnType:
    """Validate Debit response data.

    Args:
        data (dict): debit response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(DebitResponse, data)


def validate_refund_request(data: dict) -> ValidateRequestReturnType:
    """Validate Refund request data.

    Args:
        data (dict): refund request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(RefundRequest, data)


def validate_webhook_request(data: dict) -> ValidateWebhookRequestType:
    """Validate Webhook request data.

    Args:
        data (dict): webhook request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(WebhookRequest, data)


def validate_refund_response(data: dict) -> ValidateResponseReturnType:
    """Validate Refund response data.

    Args:
        data (dict): refund response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(RefundResponse, data)


def validate_webhook_response(data: dict) -> ValidateResponseReturnType:
    """Validate Webhook response data.

    Args:
        data (dict): webhook response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(WebhookResponse, data)


def validate_status_response(data: dict) -> ValidateResponseReturnType:
    """Validate Status response data.

    Args:
        data (dict): status response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(StatusResponse, data)


def validate_cancel_request(data: dict) -> ValidateRequestReturnType:
    """Validate Cancel request data.

    Args:
        data (dict): Cancel request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(CancelRequest, data)


def validate_cancel_response(data: dict) -> ValidateResponseReturnType:
    """Validate Cancel response data.

    Args:
        data (dict): Cancel response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(CancelResponse, data)


def validate_error_response(data: dict) -> ValidateResponseReturnType:
    """Validate Error response data.

    Args:
        data (dict): error response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(ErrorResponse, data)


def validate_bad_request_response(data: dict) -> ValidateResponseReturnType:
    """Validate bad request response data.

    Args:
        data (dict): bad request response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(Error400Response, data)
