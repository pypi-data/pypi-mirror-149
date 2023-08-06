from marshmallow import INCLUDE, Schema, validate
from marshmallow.fields import Dict, Nested, String, Url

from peachpayments_partner_marshmallow.fields import (
    PAYMENT_TYPE_DEBIT,
    PAYMENT_TYPE_REFUND,
    Amount,
    BankAccount,
    Cart,
    ClearingInstituteSessionId,
    ConnectorTxID1,
    Currency,
    Customer,
    CustomParameters,
    Data,
    DebitRequestCard,
    Error400Result,
    MerchantTransactionId,
    NotificationUrl,
    PaymentBrand,
    PaymentType,
    Recon,
    Redirect,
    Result,
    ResultDetails,
    StatusResponseCard,
    Timestamp,
    UniqueId,
)
from peachpayments_partner_marshmallow.validate import Regexp


class DebitRequest(Schema):
    """Represents initial debit request fields sent by Peach to Partner API."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    configuration = Dict(required=True)
    paymentType = PaymentType(required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_DEBIT))
    customer = Nested(Customer)
    customParameters = CustomParameters()
    # example: "Shopping Merchant"
    merchantName = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"), required=True)
    merchantTransactionId = MerchantTransactionId()
    # "20170630-4072-00"
    merchantInvoiceId = String(validate=Regexp(regex=r"^[\w~!@#$%\^&*()+\-,./:?\][\\\{}`;|\"']{8,255}$"))
    clearingInstituteSessionId = ClearingInstituteSessionId()
    notificationUrl = Url(required=True)
    # This will only be used to redirect back to Peach
    # example: "https://peachredirect.com/v1/redirect/paymentBrand"
    shopperResultUrl = Url(required=True)
    card = Nested(DebitRequestCard)
    billing = Nested(Data)
    shipping = Nested(Data)
    cart = Nested(Cart)

    class Meta:
        """Configuration of the DebitRequest schema."""

        unknown = INCLUDE


class DebitResponse(Schema):
    """Defines fields to be sent as a debit response."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    connectorTxID1 = ConnectorTxID1(required=True)
    timestamp = Timestamp(required=True)
    paymentType = PaymentType(required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_DEBIT))
    redirect = Nested(Redirect, required=True)
    clearingInstituteSessionId = ClearingInstituteSessionId()

    class Meta:
        """Configuration of the DebitResponse schema."""

        unknown = INCLUDE


class WebhookRequest(Schema):
    """Defines fields to be sent in a Webhook request."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    paymentType = PaymentType(required=True)
    customParameters = CustomParameters()
    clearingInstituteSessionId = ClearingInstituteSessionId()
    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    connectorTxID1 = ConnectorTxID1(required=True)
    card = Nested(StatusResponseCard)
    recon = Nested(Recon)
    bankAccount = Nested(BankAccount)
    timestamp = Timestamp(required=True)


class RefundRequest(Schema):
    """Defines fields to be sent in a Refund request."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    configuration = Dict(required=True)
    paymentType = PaymentType(required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_REFUND))
    customer = Nested(Customer())
    customParameters = CustomParameters()
    notificationUrl = NotificationUrl(required=True)

    class Meta:
        """Configuration of the RefundRequest schema."""

        unknown = INCLUDE


class RefundResponse(Schema):
    """Defines fields to be sent in a Refund response."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    connectorTxID1 = ConnectorTxID1(required=True)
    timestamp = Timestamp(required=True)
    paymentType = PaymentType(required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_REFUND))
    customParameters = CustomParameters()


class StatusResponse(Schema):
    """Defines fields to be sent in a Status response."""

    uniqueId = UniqueId(required=True)
    amount = Amount(required=True)
    currency = Currency(required=True)
    paymentBrand = PaymentBrand(required=True)
    paymentType = PaymentType(required=True)
    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    connectorTxID1 = ConnectorTxID1(required=True)
    clearingInstituteSessionId = ClearingInstituteSessionId()
    timestamp = Timestamp(required=True)
    recon = Nested(Recon)
    bankAccount = Nested(BankAccount())
    card = Nested(StatusResponseCard())
    customParameters = CustomParameters()


class CancelRequest(Schema):
    """Defines fields to be sent in a Cancel request."""

    configuration = Dict(required=True)
    paymentBrand = String(required=True, validate=Regexp(regex=r"^[a-zA-Z0-9_]{1,32}$"))
    customParameters = CustomParameters()
    notificationUrl = Url(required=True)
    timestamp = Timestamp(required=True)
    merchantTransactionId = MerchantTransactionId()
    clearingInstituteSessionId = ClearingInstituteSessionId()

    class Meta:
        """Configuration of the CancelRequest schema."""

        unknown = INCLUDE


class CancelResponse(Schema):
    """Defines fields to be sent in a Cancel response."""

    uniqueId = UniqueId(required=True)
    paymentBrand = PaymentBrand(required=True)
    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    connectorTxID1 = ConnectorTxID1(required=True)
    timestamp = Timestamp(required=True)
    customParameters = CustomParameters()


class ErrorResponse(Schema):
    """Definition of a error response."""

    result = Nested(Result, required=True)
    resultDetails = ResultDetails()
    timestamp = Timestamp(required=True)


class Error400Response(Schema):
    """Definition of the Error 400."""

    result = Nested(Error400Result, required=True)
    resultDetails = ResultDetails()
    timestamp = Timestamp(required=True)


class WebhookResponse(Schema):
    """A positive response to a request."""

    result = Nested(Result, required=True)
    timestamp = Timestamp(required=True)
