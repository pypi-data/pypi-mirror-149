"""Provides custom Marshmallow validators."""
import re

from iso4217 import Currency as IsoCurrency
from marshmallow import ValidationError
from marshmallow.validate import Regexp as RegexpValidator
from marshmallow.validate import Validator
from peachpayments_partner.result_codes import result_codes


class Currency(Validator):
    """Validate the Currency field."""

    def __call__(self, value):
        """Use IsoCurrency to validate the currency."""
        try:
            IsoCurrency(value)
        except ValueError as excinfo:
            raise ValidationError("Must be a valid ISO-4217, 3-character currency.") from excinfo


class Regexp(RegexpValidator):
    """Extends validate.Regexp to add desired error response."""

    def __init__(self, *args, **kwargs):
        """Redefine the error message."""
        super().__init__(*args, **kwargs, error="Must match {regex}")


class Code(Validator):
    """Validate result code."""

    def __init__(self, *args, **kwargs):
        """Add Regexp validation."""
        super().__init__(*args, **kwargs)
        regex = kwargs.get("regex") or r"^([0-9]{3}.[0-9]{3}.[0-9]{3})?$"
        flags = kwargs.get("flags") or 0
        self.regex = re.compile(regex, flags) if isinstance(regex, (str, bytes)) else regex

    def __call__(self, value):
        """Validate the format and then check if value belongs to existing result codes."""
        if self.regex.match(value) is None:
            raise ValidationError(f"Must match {self.regex.pattern}")

        try:
            result_codes.get(value)
        except KeyError as excinfo:
            raise ValidationError(f'Unknown result code "{value}".') from excinfo
