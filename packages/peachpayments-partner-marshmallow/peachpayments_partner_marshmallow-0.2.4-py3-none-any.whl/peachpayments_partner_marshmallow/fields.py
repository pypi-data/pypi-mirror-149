"""Provides custom Marshmallow fields."""

from marshmallow import INCLUDE, Schema, validate
from marshmallow.fields import IP, UUID, DateTime, Dict, Email, Field, List, Nested, String, Url

from peachpayments_partner_marshmallow.validate import Code as CodeValidator
from peachpayments_partner_marshmallow.validate import Currency as CurrencyValidator
from peachpayments_partner_marshmallow.validate import Regexp

PAYMENT_TYPE_DEBIT = "DB"
PAYMENT_TYPE_REFUND = "RF"
TRUE = "true"
FALSE = "false"


class CustomParameters(Dict):
    """A JSON object depicting custom information sent by the merchant and Peach.

    This needs to be collected in request and echoed back in the responses.
    """

    def __init__(self, *args, **kwargs):
        """Forcing keys as strings."""
        super().__init__(keys=String(), values=Field(), *args, **kwargs)


class ResultDetails(Dict):
    """Details that can help understanding the reason for error, can be empty for successful transactions."""

    def __init__(self, *args, **kwargs):
        """Forcing keys as strings."""
        super().__init__(keys=String(), values=Field(), *args, **kwargs)


class ParameterError(Schema):
    """Defines ErrorParameter fields to be sent in a Bad request response."""

    # The value of the parameter which failed validation. Can be any value - string, number, boolean, array or object.
    value = Field(required=True, allow_none=True)
    # The name of the parameter.
    name = String(required=True)
    # A message describing the error.
    message = String(required=True)


class ParameterErrors(List):
    """List of ParameterError objects.

    example: [
      {"value": "null", "name": "authenticationValue", "message": "Partner API requires authenticationValue"}
    ]
    """

    def __init__(self, *args, required=False, **kwargs) -> None:
        """Defining the list items of ParameterErrors."""
        super().__init__(Nested(ParameterError), *args, required=required, **kwargs)


class ExpiryMonth(String):
    """The expiry month of the card.

    The value must be between 1 and 12.

    example: "01"
    """

    def __init__(self, *args, **kwargs):
        """Defining the Regexp validation."""
        super().__init__(*args, validate=Regexp(regex=r"^(0[1-9]|1[0-2])$"), **kwargs)


class ExpiryYear(String):
    """The expiry year of the card.

    The value must be between the current year and 2099.

    example: "2030"
    """

    def __init__(self, *args, **kwargs):
        """Defining the Regexp validation."""
        super().__init__(*args, validate=Regexp(regex=r"^(20)([0-9]{2})$"), **kwargs)


class Holder(String):
    """Holder of the credit card account.

    example: "John Doe"
    """

    def __init__(self, *args, **kwargs):
        """Defining the Regexp validation."""
        super().__init__(
            *args, validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$"), **kwargs
        )


class DebitRequestCard(Schema):
    """The card data structure holds all information regarding a credit or debit card account."""

    # The PAN or account number of the card.
    # example: "4242424242424242"
    number = String(required=True, validate=Regexp(regex=r"^[0-9]{12,19}$"))
    # The card security code or CVV.
    # example: "123"
    cvv = String(validate=Regexp(regex=r"^[0-9]{3,4}$"))
    holder = Holder()
    expiryMonth = ExpiryMonth(required=True)
    expiryYear = ExpiryYear(required=True)


class StatusResponseCard(Schema):
    """The card data structure holds all information regarding a credit or debit card account."""

    # The first six digits of the card number.
    # example: "455112"
    bin = Field(validate=Regexp("^[\\d]{6}$"))
    # Last 4 digits of the credit/debit card.
    # example: "2315"
    last4Digits = Field(validate=Regexp("^[\\d]{4}$"))
    # Holder of the credit card account.
    # example: "Jane Doe"
    holder = Holder()
    # The expiry month of the card.
    # example: "01"
    expiryMonth = ExpiryMonth()
    # The expiry year of the card.
    # example: "2030"
    expiryYear = ExpiryYear()


class Mandate(Schema):
    """Customer mandate to bank."""

    # The date the direct debit mandate was signed.
    dateOfSignature = String(
        validate=Regexp(regex=r"^(19|20)([0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$")
    )
    # The id of the mandate for direct debit.
    id = String(validate=Regexp(regex=r"^[a-zA-Z0-9]{35}$"))
    # The mandate reference for direct debit as a contractual agreement between the creditor and the debtor.
    reference = String(validate=Regexp(regex=r"^[a-zA-Z0-9]{32}$"))


class Recon(Schema):
    """The transaction reconciliation data."""

    # The clearing institute merchant number.
    ciMerchantNumber = String(validate=Regexp(regex=r"^[\s\S]{1,128}$"))
    # The recon reference number from the bank.
    rrn = String(validate=Regexp(regex=r"^[\s\S]{1,128}$"))
    # The stan reference number from the bank.
    stan = String(validate=Regexp(regex=r"^[\s\S]{1,128}$"))
    # The auth code returned from the bank.
    authCode = String(validate=Regexp(regex=r"^[\s\S]{1,128}$"))
    # The result code provided by the bank.
    resultCode = String(validate=Regexp(regex=r"^[\s\S]{1,128}$"))


class Amount(String):
    """Indicates the amount of the payment request.

    example: "22.50"
    """

    def __init__(self, *args, **kwargs):
        """Forcing Regexp validation."""
        super().__init__(*args, validate=Regexp(regex=r"^[0-9]{1,10}(\.[0-9]{2})$"), **kwargs)


class Currency(String):
    """The currency code of the payment request's amount.

    example: "ZAR"
    """

    def __init__(self, *args, **kwargs):
        """Forcing Currency validation."""
        super().__init__(*args, validate=CurrencyValidator(), **kwargs)


class PaymentBrand(String):
    """The payment brand specifies the method of payment for the request.

    example: VISA
    """

    def __init__(self, *args, **kwargs):
        """Forcing Regexp validation."""
        super().__init__(*args, validate=Regexp(regex="^[a-zA-Z0-9_]{1,32}$"), **kwargs)


class UniqueId(UUID):
    """The unique transaction ID provided by Peach.

    example: "b4508276b8d146728dac871d6f68b45d"
    """


class ConnectorTxID1(String):
    """A unique transaction identifier provided by the Partner.

    example: "8ac7a49f7921f2fd0179230196ec4bbe"
    """

    def __init__(self, *args, **kwargs):
        """Forcing Regexp validation."""
        super().__init__(*args, validate=Regexp(regex=r"^[\S]{1,64}$"), **kwargs)


class PaymentType(String):
    """Payment type of the transaction."""

    def __init__(self, *args, **kwargs):
        """Forcing PaymentType validation."""
        kwargs["validate"] = kwargs.get("validate") or validate.OneOf(choices=[PAYMENT_TYPE_REFUND, PAYMENT_TYPE_DEBIT])
        super().__init__(*args, **kwargs)


class Code(String):
    """The unique code that indicates the result status of the request.

    example: "800.100.153"
    """

    def __init__(self, *args, **kwargs):
        """Forcing CodeValidator validation."""
        super().__init__(*args, validate=CodeValidator(), **kwargs)


class Timestamp(DateTime):
    """A timestamp of the transaction.

    example: "2021-04-23T07:41:25.519947Z"
    """


class NotificationUrl(Url):
    """The Peach provided URL.

    Partner is required to send notifications/webhooks to the URL when the transaction status is updated.

    example: "https://peachnotify.com"
    """


class MerchantTransactionId(String):
    """Merchant-provided reference number. This identifier is often used for reconciliation.

    example: "test-12345"
    """

    def __init__(self, *args, **kwargs):
        """Forcing Regexp validation."""
        super().__init__(*args, validate=Regexp(regex=r"^[\s\S]{1,255}$"), **kwargs)


class ClearingInstituteSessionId(String):
    """Session ID of the transaction, provided by the Partner.

    example: "6262"
    """

    def __init__(self, *args, **kwargs):
        """Forcing Regexp validation."""
        super().__init__(*args, validate=kwargs.get("validate") or Regexp(regex=r"^[\s\S]{1,32}$"), **kwargs)


class Result(Schema):
    """Result of the transaction."""

    code = Code(required=True)


class Browser(Schema):
    """Optional object sent if Partner requires browser data."""

    # Value of the Accept header sent from the customer's browser.
    # example: "application/json"
    acceptHeader = String(validate=Regexp(regex=r"^[\s\S]{1,2048}$"))
    # Value representing the browser language as defined in IETF BCP47.
    # example: "EN"
    language = String(validate=Regexp(regex=r"^[\s\S]{1,8}$"))
    # Total height of the customer’s screen in pixels.
    # example: "1080"
    screenHeight = String(validate=Regexp(regex=r"^[\s\S]{1,6}$"))
    # Total width of the customer’s screen in pixels.
    # example: "1920"
    screenWidth = String(validate=Regexp(regex=r"^[\s\S]{1,6}$"))
    # Time-zone offset in minutes between UTC and the customer's browser's local time.
    # example: "30"
    timezone = String(validate=Regexp(regex=r"^[\s\S]{1,5}$"))
    # Exact content of the HTTP user-agent header.
    # example: "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"
    userAgent = String(validate=Regexp(regex=r"^[\s\S]{1,2048}$"))
    # Boolean that represents the ability of the customer's browser to execute Java.
    # example: "false"
    javaEnabled = String(validate=validate.OneOf([TRUE, FALSE]))
    # Boolean that represents the ability of the customer's browser to execute javascript.
    # example: "true"
    javascriptEnabled = String(validate=validate.OneOf([TRUE, FALSE]))
    # Value representing the bit depth of the colour palette for displaying images, in bits per pixel.
    # example: "24"
    screenColorDepth = String(validate=Regexp(regex=r"^[0-9]{1,2}$"))
    # Dimensions of the challenge window that has been displayed to the customer.
    # example: "640x480"
    challengeWindow = String(validate=Regexp(regex=r"^[0-9]{1,2}$"))


class Customer(Schema):
    """Optional object sent if Partner requires customer data."""

    # The customer's email  address.
    # example: "name@example.com"
    email = Email(validate=validate.Length(min=6, max=128))
    # The customer's fax number if provided.
    # example: "2919392022"
    fax = String(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{7,25}$"))
    # The first name or given name of the customer.
    # example: "Jane"
    givenName = String(validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$"))
    # The last name or surname of the customer.
    # example: "Doe"
    surname = String(validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$"))
    # The customer's mobile phone number.
    # example: "27610107822"
    mobile = String(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{5,25}$"))
    # The customer's phone number.
    # example: "27210030000"
    phone = String(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{7,25}$"))
    # The customer's IP address.
    # example: "0.0.0.0"
    ip = IP()
    # The language used for the customer on the merchant's site.
    # example: "EN"
    merchantCustomerLanguage = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # This is used to determine if this is a new customer or an return customer
    # example: "NEW"
    status = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The customer's ID on the merchant's site.
    # example: "sxxopjqy"
    merchantCustomerId = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The customer's tax id if required.
    # example: "4550045030303"
    taxId = String(validate=Regexp(regex=r"^[\s\S]{1,100}$"))
    # The customer's tax type if required.
    # example: "tax type"
    taxType = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The customer's birth date.
    # example: "1996-08-07"
    birthDate = String(validate=Regexp(regex=r"^(19|20)([0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"))
    # Customer's browser details.
    browser = Nested(Browser)

    class Meta:
        """Configuration of the Customer schema."""

        unknown = INCLUDE


class BankAccount(Schema):
    """Optional object that can be used for bank account data."""

    # Holder of the bank account.
    # example: John Doe
    holder = String(validate=Regexp(regex=r"^[\s\S]{4,128}$"))
    # The name of the bank which holds the account.
    # example: "Barclays Bank"
    bankName = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The account number of the bank account.
    number = String(validate=Regexp(regex=r"^[a-zA-Z0-9]{3,64}$"))
    # The IBAN (International Bank Account Number) associated with the bank account.
    iban = String(validate=Regexp(regex=r"^[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{11,27}$"))
    # The BIC (Bank Identifier Code (SWIFT)) number of the bank account.
    bic = String(validate=Regexp(regex=r"^[a-zA-Z0-9]{8}|[a-zA-Z0-9]{11}$"))
    # The code associated with the bank account.
    bankCode = String(validate=Regexp(regex=r"^[a-zA-Z0-9]{1,12}$"))
    # The country code of the bank account (ISO 3166-1).
    country = String(validate=Regexp(regex=r"^[a-zA-Z]{2}$"))
    mandate = Nested(Mandate)
    # The due date of the transaction of the direct debit.
    transactionDueDate = String(
        validate=Regexp(regex=r"^(19|20)([0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$")
    )


class Data(Schema):
    """Optional object that can be used for billing/shipping information."""

    # The town, district or city linked to billing/shipping.
    # example: "Cape Town"
    city = String(validate=Regexp(regex=r"^[\s\S]{1,48}$"))
    # The customer's company name.
    # "Company name"
    company = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The country linked to billing/shippin.
    # example: "ZA"
    country = String(validate=Regexp(regex=r"^[A-Z]{2}$"))
    # Primary house number of the billing/shipping address.
    # example: "25567"
    houseNumber1 = String(validate=Regexp(regex=r"^[\s\S]{1,100}$"))
    # The postal code or zip code of the billing/shipping address.
    # example: "8001"
    postcode = String(validate=Regexp(regex=r"^[\s\S]{1,16}$"))
    # The county, state or region of the billing address.
    # example: "Nasarawa"
    state = String(validate=Regexp(regex=r"^[a-zA-Z0-9\.]{1,10}$"))
    # The door number, floor, building number, building name, and/or street name of the billing/shipping address.
    # example: "Langtree Lane"
    street1 = String(validate=Regexp(regex=r"^[\s\S]{1,95}$"))
    # Secondary house number of the billing/shipping address. Used when more addresses are bundled to a same
    # primary house number. If present,houseNumber1 is also mandatory.
    # example: "Loe Street"
    street2 = String(validate=Regexp(regex=r"^[\s\S]{1,95}$"))
    customer = Nested(Customer)

    class Meta:
        """Configuration of the Data schema."""

        unknown = INCLUDE


class CartItem(Schema):
    """Optional object that can be used for cart Item data."""

    # The name of the item in the shopping cart.
    # example: "Laptop"
    name = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The unique identifier of the item in the shopping cart.
    # example: "item123"
    merchantItemId = String(validate=Regexp(regex=r"^[\s\S]{1,255}$"))
    # The number of items in the shopping cart.
    # "125"
    quantity = String(validate=Regexp(regex=r"^[1-9][0-9]{0,11}$"))
    # The price of the item in the shopping cart.
    # example: "12.50"
    price = String(validate=Regexp(regex=r"^[0-9]{1,10}\.[0-9]{2}$"))
    # The description of the item in the shopping cart.
    description = String(validate=Regexp(regex=r"^[\s\S]{1,2048}$"))
    # The weight (in kg) of the item in the shopping cart.
    # example: "05.25"
    weightInKg = String(validate=Regexp(regex=r"^[0-9]{1,10}\.[0-9]{2}$"))
    # The category of the item in the shopping cart.
    # example: "electronics"
    category = String(validate=Regexp(regex=r"^[\s\S]{1,2048}$"))


class Cart(Schema):
    """Optional object that can be used for cart data."""

    # Details of the items in the cart.
    cartItems = List(Nested(CartItem))
    # The tax percentage applied to the price of the item in the shopping cart.
    tax = String(validate=Regexp(regex=r"^[0-9]{1,8}(\.[0-9]{2})?$"))
    # The shipping amount applied to the item in the shopping cart.
    # example: "12.50"
    shippingAmount = String(validate=Regexp(regex=r"^[0-9]{1,10}\.[0-9]{2}$"))
    # The discount percentage applied to the price of the item in the shopping cart.
    # example: "02.25"
    discount = String(validate=Regexp(regex=r"^[0-9]{1,10}\.[0-9]{2}$"))


class Parameter(Schema):
    """Parameters sent in the redirect object."""

    name = String(required=True)
    value = String(required=True)


class Redirect(Schema):
    """Fields used to provide the redirect information."""

    # URL the the shopper must be redirected to in order to proceed.
    # example: "https://test.yourdomain.com/link?"
    url = Url(required=True)
    # Array of parameter names and values for the redirect url.
    parameters = List(Nested(Parameter), required=True)
    # REST method used for redirection
    # example: "POST"
    method = String(required=True, validate=validate.OneOf(choices=["GET", "POST"]))


class Error400Result(Schema):
    """Definition of the Error 400."""

    code = Code(required=True)
    parameterErrors = ParameterErrors(required=True)
