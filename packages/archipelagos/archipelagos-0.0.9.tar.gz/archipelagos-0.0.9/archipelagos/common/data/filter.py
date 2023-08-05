"""
Classes and functions used when processing filters.
"""
from archipelagos.common.data import is_valid_token, parse_timestamp_str

from abc import ABC, abstractmethod
from pandas import Timestamp
from typing import Any
from enum import Enum
import datetime


class Symbol(ABC):
    """
    Needs to be implemented by all symbols.
    """
    def __str__(self) -> str:
        """
        """
        pass


class LeftBracket(Symbol):
    """
    Represents a left bracket (parenthesis).
    """
    def __str__(self) -> str:
        """
        """
        return "("


class RightBracket(Symbol):
    """
    Represents a right bracket (parenthesis).
    """
    def __str__(self) -> str:
        """
        """
        return ")"


class ConstantType(Enum):
    """
    The different types of arguments that may be present in a simple filter.
    """
    STRING = 0
    BOOL = 1
    INT = 2
    DOUBLE = 3
    DATE_TIME = 4
    FEATURE = 5


class Constant(Symbol):
    """
    Should be implemented by all constants.
    """
    @abstractmethod
    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        pass

    @abstractmethod
    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        pass


class BooleanConstant(Constant):
    """
    Represents a Boolean constant.
    """
    def __init__(self,
                 text: str,
                 value: bool):
        """
        :param text: The string representation of the operator.
        :type text: str

        :param value: The value of the constant.
        :type value: bool
        """
        self._text = text
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.BOOL

    def __str__(self) -> str:
        """
        """
        return self._text


class StringConstant(Constant):
    """
    Represents a String constant.
    """
    def __init__(self,
                 value: str):
        """
        :param value: The value of the constant.
        :type value: str
        """
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.STRING

    def __str__(self) -> str:
        """
        """
        return self._value


class IntegerConstant(Constant):
    """
    Represents an integer constant.
    """
    def __init__(self,
                 text: str,
                 value: int):
        """
        :param text: The string representation of the constant.
        :type text: str

        :param value: The value of the constant.
        :type value: int
        """
        self._text = text
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.INT

    def __str__(self) -> str:
        """
        """
        return self._text


class DoubleConstant(Constant):
    """
    Represents a double constant.
    """
    def __init__(self,
                 text: str,
                 value: float):
        """
        :param text: The string representation of the constant.
        :type text: str

        :param value: The value of the constant.
        :type value: float
        """
        self._text = text
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.DOUBLE

    def __str__(self) -> str:
        """
        """
        return self._text


class FeatureReference(Constant):
    """
    Represents a feature reference.
    """
    def __init__(self,
                 value: str):
        """
        :param value: The value of the constant.
        :type value: str
        """
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.FEATURE

    def __str__(self) -> str:
        """
        """
        return self._value


class DateTimeConstant(Constant):
    """
    Represents a date/time constant.
    """
    def __init__(self,
                 text: str,
                 value: datetime.date):
        """
        :param text: The string representation of the constant.
        :type text: str

        :param value: The value of the constant.
        :type value: Timestamp
        """
        self._text = text
        self._value = value

    def value(self) -> Any:
        """
        :return: The value of the constant.
        :rtype: Any
        """
        return self._value

    def constant_type(self) -> ConstantType:
        """
        :return: The type of the constant.
        :rtype: ConstantType
        """
        return ConstantType.DATE_TIME

    def __str__(self) -> str:
        """
        """
        return self._text


class OperatorType:
    """
    The different types of operators that may be present in a filter.
    """
    def __init__(self,
                 operator: str):
        """
        :param operator: The operator.
        :type operator: str
        """
        self._operator = operator

    def __str__(self) -> str:
        """
        """
        return self._operator


class OperatorTypes:
    """
    The different types of operators supported.
    """
    EQUALS = OperatorType("=")
    NOT_EQUALS = OperatorType("!=")
    GREATER_THAN = OperatorType(">")
    GREATER_THAN_OR_EQUALS = OperatorType(">=")
    LESS_THAN = OperatorType("<")
    LESS_THAN_OR_EQUALS = OperatorType("<=")
    LIKE = OperatorType("like")
    UNLIKE = OperatorType("unlike")
    NOT = OperatorType("not")
    AND = OperatorType("and")
    OR = OperatorType("or")


class Operator(Symbol):
    """
    Should be extended by all operators.
    """
    @property
    @abstractmethod
    def operator_type(self) -> OperatorType:
        """
        The type of the operator.
        """
        pass


class ComparisonOperator(Operator):
    """
    Represents a comparison operator (e.g. <=, =, like...).
    """
    def __init__(self,
                 text: str,
                 operator_type: OperatorType):
        """
        :param text: The string representation of the operator.
        :type text: str

        :param operator_type: The type of the operator.
        :type operator_type: OperatorType
        """
        self._text = text
        self._operator_type = operator_type

    def operator_type(self) -> OperatorType:
        """
        The type of the operator.
        """
        return self._operator_type

    def __str__(self) -> str:
        """
        """
        return self._text


class LogicalOperator(Operator):
    """
    Represents a logical operator (e.g. AND, OR, NOT...).
    """
    def __init__(self,
                 text: str,
                 operator_type: OperatorType):
        """
        :param text: The string representation of the operator.
        :type text: str

        :param operator_type: The type of the operator.
        :type operator_type: OperatorType
        """
        self._text = text
        self._operator_type = operator_type

    def operator_type(self) -> OperatorType:
        """
        The type of the operator.
        """
        return self._operator_type

    def __str__(self) -> str:
        """
        """
        return self._text


class Expression(ABC):
    """
    Should be implemented by all expressions.
    """
    pass


class BooleanExpression(Expression):
    """
    Should be implemented by all expressions that result in Booleans.
    """
    pass


class NotExpression(BooleanExpression):
    """
    Represents a NOT expression.
    """
    def __init__(self,
                 operator: LogicalOperator,
                 expression: BooleanExpression):
        """
        :param operator: The not operator.
        :type operator: LogicalOperator

        :param expression: The Boolean expression that this negates.
        :type expression: BooleanExpression
        """
        if OperatorTypes.NOT != operator.operator_type():
            raise ValueError(f"operator is not of type \"{OperatorTypes.NOT}\"")

        self._operator = operator
        self._expression = expression

    def operator(self) -> LogicalOperator:
        """
        :return: The not operator.
        :rtype: LogicalOperator
        """
        return self._operator

    def expression(self) -> BooleanExpression:
        """
        :return: The Boolean expression that this negates.
        :rtype: BooleanExpression
        """
        return self._expression


class AndExpression(BooleanExpression):
    """
    Represents a NOT expression.
    """
    def __init__(self,
                 left_expression: BooleanExpression,
                 operator: LogicalOperator,
                 right_expression: BooleanExpression):
        """
        :param left_expression: The left-hand logical expression that the expression is composed of.
        :type left_expression: BooleanExpression

        :param operator: The operator that the expression is composed of.
        :type operator: LogicalOperator

        :param right_expression: The right-hand logical expression that the expression is composed of.
        :type right_expression: BooleanExpression
        """
        self._left_expression = left_expression
        self._operator = operator
        self._right_expression = right_expression

    def operator(self) -> LogicalOperator:
        """
        :return: The not operator.
        :rtype: LogicalOperator
        """
        return self._operator

    def left_expression(self) -> BooleanExpression:
        """
        :return: The left-hand logical expression that the expression is composed of.
        :rtype: BooleanExpression
        """
        return self._left_expression

    def right_expression(self) -> BooleanExpression:
        """
        :return: The right-hand logical expression that the expression is composed of.
        :rtype: BooleanExpression
        """
        return self._right_expression


class OrExpression(BooleanExpression):
    """
    Represents an OR expression.
    """
    def __init__(self,
                 left_expression: BooleanExpression,
                 operator: LogicalOperator,
                 right_expression: BooleanExpression):
        """
        :param left_expression: The left-hand logical expression that the expression is composed of.
        :type left_expression: BooleanExpression

        :param operator: The operator that the expression is composed of.
        :type operator: LogicalOperator

        :param right_expression: The right-hand logical expression that the expression is composed of.
        :type right_expression: BooleanExpression
        """
        self._left_expression = left_expression
        self._operator = operator
        self._right_expression = right_expression

    def operator(self) -> LogicalOperator:
        """
        :return: The not operator.
        :rtype: LogicalOperator
        """
        return self._operator

    def left_expression(self) -> BooleanExpression:
        """
        :return: The left-hand logical expression that the expression is composed of.
        :rtype: BooleanExpression
        """
        return self._left_expression

    def right_expression(self) -> BooleanExpression:
        """
        :return: The right-hand logical expression that the expression is composed of.
        :rtype: BooleanExpression
        """
        return self._right_expression


class ComparisonExpression(BooleanExpression):
    """
    Represents an expression composed of a comparison operator followed by a constant.
    """
    def __init__(self,
                 operator: ComparisonOperator,
                 constant: Constant):
        """
        :param operator: The not operator.
        :type operator: LogicalOperator

        :param constant: The constant that the expression is composed of.
        :type constant: Constant
        """
        self._operator = operator
        self._constant = constant

    def operator(self) -> ComparisonOperator:
        """
        :return: The not operator.
        :rtype: ComparisonOperator
        """
        return self._operator

    def constant(self) -> Constant:
        """
        :return: The constant that the expression is composed of.
        :rtype: Constant
        """
        return self._constant


class _ProcessingResult:
    """
    Represents the result of processing a potential symbol.
    """
    def __init__(self,
                 constant_type: ConstantType = None,
                 text: str = None,
                 remainder: str = None,
                 error_occurred: bool = False,
                 error_message: str = None):
        """
        :param constant_type: The type of constant found.
        :type constant_type: ConstantType

        :param text: The constant.
        :type text: str

        :param remainder: The remainder of the input left to process.
        :type remainder: str

        :param error_occurred: bool
        :type error_occurred: bool

        :param error_message: The error message.
        :type error_message: str
        """
        self._constant_type = constant_type
        self._text = text
        self._remainder = remainder
        self._error_occurred = error_occurred
        self._error_message = error_message

    @property
    def constant_type(self) -> ConstantType:
        """
        :return: v
        :rtype: ConstantType
        """
        return self._constant_type

    @property
    def text(self) -> str:
        """
        :return: The constant.
        :rtype: str
        """
        return self._text

    @property
    def remainder(self) -> str:
        """
        :return: The remainder of the input left to process.
        :rtype: str
        """
        return self._remainder

    @property
    def error_occurred(self) -> bool:
        """
        :return: True if an error occurred, False otherwise.
        :rtype: bool
        """
        return self._error_occurred

    @property
    def error_message(self) -> str:
        """
        :return: The error message.
        :rtype: str
        """
        return self._error_message


class LexicalParser:
    """
    The lexical parser for filters.
    """
    _TRUE_CONSTANT = "true"
    _FALSE_CONSTANT = "false"
    _LEFT_BRACKET = "("
    _RIGHT_BRACKET = ")"

    def __init__(self,
                 to_parse: str):
        """
        :param to_parse: The input to parse.
        :type to_parse: str
        """
        if to_parse is None or len(to_parse) == 0:
            raise ValueError("no input has been given")

        self._remainder = to_parse

    @staticmethod
    def _process_feature_reference(remainder: str) -> _ProcessingResult:
        """
        Process a feature reference symbol.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in all the features (that can be separated by '.')

        feature = ""
        remainder_len = len(remainder)
        pos = 0

        while True:
            # See if we need to add a period

            if pos < remainder_len and remainder[pos] == '.':
                feature += "."
                pos += 1

            # Read in a token

            token = ""

            while pos < remainder_len and (str.isalpha(remainder[pos]) or str.isdigit(remainder[pos]) or remainder[pos] == '_' or remainder[pos] == '-'):
                token += remainder[pos]
                pos += 1

            # Check that the token is valid

            if not is_valid_token(token):
                error_message = "the filter contains an unrecognised constant"
                return _ProcessingResult(error_occurred=True, error_message=error_message)
            else:
                feature += token

            if pos >= remainder_len or remainder[pos] != '.':
                break

        # Return the result

        constant_type = ConstantType.FEATURE
        feature_len = len(feature)
        remainder = remainder[feature_len:] if feature_len < remainder_len else ""

        return _ProcessingResult(constant_type=constant_type, text=feature, remainder=remainder)

    @staticmethod
    def _process_datetime(remainder: str) -> _ProcessingResult:
        """
        Process a date/time symbol.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in the year part

        date_time = ""
        year_part = ""
        remainder_len = len(remainder)
        pos = 0

        while pos < remainder_len and str.isdigit(remainder[pos]):
            date_time += remainder[pos]
            year_part += remainder[pos]
            pos += 1

        # Date/times must started with 4 digits (the year) and a hyphen

        if pos < remainder_len and len(year_part) == 4 and remainder[pos] == '-':
            date_time += '-'
            pos += 1

            # Read in the month part

            month_part = ""

            while pos < remainder_len and str.isdigit(remainder[pos]):
                date_time += remainder[pos]
                month_part += remainder[pos]
                pos += 1

            # The year part must be followed by a 1 or 2 digit month

            month_part_len = len(month_part)

            if pos < remainder_len and month_part_len > 0 and month_part_len < 3 and remainder[pos] == '-':
                date_time += '-'
                pos += 1

                # Check the month number is valid

                month = int(month_part)

                if month >= 1 and month <= 12:
                    # Read in the day part

                    day_part = ""

                    while pos < remainder_len and str.isdigit(remainder[pos]):
                        date_time += remainder[pos]
                        day_part += remainder[pos]
                        pos += 1

                    # The month part must be followed by a 1 or 2 digit day

                    day_part_len = len(day_part)

                    if day_part_len > 0 and day_part_len < 3:
                        day = int(day_part)

                        if day >= 1 and day <= 31:
                            # Check if we just have a date part, or a time part as well

                            if pos < remainder_len and remainder[pos] == 'T':
                                date_time += 'T'
                                pos += 1

                                # Read in the hour part

                                hour_part = ""

                                while pos < remainder_len and str.isdigit(remainder[pos]):
                                    date_time += remainder[pos]
                                    hour_part += remainder[pos]
                                    pos += 1

                                # Hour parts must be 1 or 2 digits followed by a colon

                                hour_part_len = len(hour_part)

                                if pos < remainder_len and (hour_part_len == 1 or hour_part_len == 2) and remainder[pos] == ":":
                                    date_time += ':'
                                    pos += 1

                                    # Check the minute number is valid

                                    hour = int(hour_part)

                                    if hour >= 0 and hour <= 23:
                                        # Read in the minute part

                                        minute_part = ""

                                        while pos < remainder_len and str.isdigit(remainder[pos]):
                                            date_time += remainder[pos]
                                            minute_part += remainder[pos]
                                            pos += 1

                                        # The minute part must be 1 or 2 digits and followed by a colon

                                        minute_part_len = len(minute_part)

                                        if pos < remainder_len and minute_part_len >0 and minute_part_len < 3 and remainder[pos] == ":":
                                            date_time += ':'
                                            pos += 1

                                            # Check the minute number is valid

                                            minute = int(minute_part)

                                            if minute >= 0 and minute <= 59:
                                                # Read in the second part

                                                second_part = ""

                                                while pos < remainder_len and str.isdigit(remainder[pos]):
                                                    date_time += remainder[pos]
                                                    second_part += remainder[pos]
                                                    pos += 1

                                                #  The second part must be 1 or 2 digits

                                                second_part_len = len(second_part)

                                                if second_part_len > 0 and second_part_len < 3:
                                                    second = int(second_part)

                                                    if second >= 0 and second <= 59:
                                                        # Check if we have a nanosecond part as well

                                                        if pos < remainder_len and remainder[pos] == ".":
                                                            date_time += '.'
                                                            pos += 1

                                                            # Read in the nanosecond part

                                                            nanosecond_part = ""

                                                            while pos < remainder_len and str.isdigit(remainder[pos]):
                                                                date_time += remainder[pos]
                                                                nanosecond_part += remainder[pos]
                                                                pos += 1

                                                            # The nanosecond part can be up to 9 digits

                                                            nanosecond_part_len = len(nanosecond_part)

                                                            if nanosecond_part_len > 0 and nanosecond_part_len < 10:
                                                                constant_type = ConstantType.DATE_TIME
                                                                argument_len = len(date_time)
                                                                remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                                                                return _ProcessingResult(constant_type=constant_type, text=date_time, remainder=remainder)

                                                            else:
                                                                error_message = "date/times must have nanoseconds between 0 and 999999999"
                                                                return _ProcessingResult(error_occurred=True, error_message=error_message)

                                                        else:
                                                            constant_type = ConstantType.DATE_TIME
                                                            argument_len = len(date_time)
                                                            remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                                                            return _ProcessingResult(constant_type=constant_type, text=date_time, remainder=remainder)

                                                    else:
                                                        error_message = "date/times must have seconds between 0 and 59"
                                                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                                                else:
                                                    error_message = "the second part of a date/time must be 1 or 2 digits"
                                                    return _ProcessingResult(error_occurred=True, error_message=error_message)

                                            else:
                                                error_message = "date/times must have minutes between 0 and 59"
                                                return _ProcessingResult(error_occurred=True, error_message=error_message)

                                        else:
                                            error_message = "the minute part of a date/time must be 1 or 2 digits followed by a colon"
                                            return _ProcessingResult(error_occurred=True, error_message=error_message)

                                    else:
                                        error_message = "date/times must have hours between 0 and 23"
                                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                                else:
                                    error_message = "the hour part of a date/time must be 1 or 2 digits followed by a colon"
                                    return _ProcessingResult(error_occurred=True, error_message=error_message)
                            else:
                                constant_type = ConstantType.DATE_TIME
                                argument_len = len(date_time)
                                remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                                return _ProcessingResult(constant_type=constant_type, text=date_time, remainder=remainder)

                        else:
                            error_message = "date/times must have days between 1 and 31"
                            return _ProcessingResult(error_occurred=True, error_message=error_message)

                    else:
                        error_message = "the day of month in a date/time must be of 1 or 2 digits and follow a hyphen"
                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                else:
                    error_message = "date/times must have months between 1 and 12"
                    return _ProcessingResult(error_occurred=True, error_message=error_message)

            else:
                error_message = "date/times must start with a four digit year followed by a hyphen and a one or two digit month"
                return _ProcessingResult(error_occurred=True, error_message=error_message)

        else:
            error_message = "date/times must start with a four digit year followed by a hyphen"
            return _ProcessingResult(error_occurred=True, error_message=error_message)

    @staticmethod
    def _process_number_argument(remainder: str) -> _ProcessingResult:
        """
        Process a number symbol.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in the integer part

        number = ""
        remainder_len = len(remainder)
        pos = 0

        while pos < remainder_len and (str.isdigit(remainder[pos]) or remainder[pos] == '_'):
            if remainder[pos] == '_':
                number_len = len(number)

                if number_len == 0:
                    error_message = "numbers cannot start with an underscore"
                    return _ProcessingResult(error_occurred=True, error_message=error_message)
                else:
                    last_char = number[number_len - 1]

                    if not str.isdigit(last_char) and last_char != '_':
                        error_message = "underscores can only follow digits or underscores in numbers"
                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                    elif pos == remainder_len-1:
                        error_message = "numbers cannot end with an underscore"
                        _ProcessingResult(error_occurred=True, error_message=error_message)

            number += remainder[pos]
            pos += 1

        # See if we have a fractional part and/or scientific notation

        if pos == remainder_len:
            constant_type = ConstantType.INT
            argument_len = len(number)
            remainder = remainder[argument_len:] if argument_len < remainder_len else ""

            return _ProcessingResult(constant_type=constant_type, text=number, remainder=remainder)

        elif pos < remainder_len and remainder[pos] == '.':
            if remainder[pos - 1] == '_':
                error_message = "underscores cannot appear directly before the decimal point in a number"
                return _ProcessingResult(error_occurred=True, error_message=error_message)

            number += '.'
            pos += 1

            # Read in the fractional part (which can just be a '.')

            while pos < remainder_len and (str.isdigit(remainder[pos]) or remainder[pos] == '_'):
                if remainder[pos] == '_':
                    number_len = len(number)
                    last_char = number[number_len - 1]

                    if not str.isdigit(last_char) and last_char != '_':
                        error_message = "underscores can only follow digits or underscores in numbers"
                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                    elif pos == remainder_len - 1:
                        error_message = "numbers cannot end with an underscore"
                        return _ProcessingResult(error_occurred=True, error_message=error_message)

                number += remainder[pos]
                pos += 1

            # Check if we have scientific notation (which must be an integer, possibly starting with '-')

            if pos < remainder_len and (remainder[pos] == 'e' or remainder[pos] == 'E'):
                if remainder[pos - 1] == '_':
                    error_message = "underscores cannot appear directly before an 'e' or 'E' in a number"
                    return _ProcessingResult(error_occurred=True, error_message=error_message)

                number += remainder[pos]
                pos += 1

                # Check if we have a negative exponent

                if pos < remainder_len and remainder[pos] == '-':
                    number += "-"
                    pos += 1

                # Check that an integer appears after the 'e' or 'E' character

                if pos >= remainder_len:
                    error_message = "scientific notation requires an integer to appear after the 'e' or 'E'"
                    return _ProcessingResult(error_occurred=True, error_message=error_message)

                elif not str.isdigit(remainder[pos]):
                    error_message = "scientific notation requires an integer to appear after the 'e' or 'E'"
                    return _ProcessingResult(error_occurred=True, error_message=error_message)

                else:
                    # Read in the exponent

                    while pos < remainder_len and (str.isdigit(remainder[pos]) or remainder[pos] == '_'):
                        if remainder[pos] == '_':
                            number_len = len(number)
                            last_char = number[number_len - 1]

                            if not str.isdigit(last_char) and last_char != '_':
                                error_message = "underscores can only follow digits or underscores in numbers"
                                return _ProcessingResult(error_occurred=True, error_message=error_message)

                            elif pos == remainder_len - 1:
                                error_message = "numbers cannot end with an underscore"
                                return _ProcessingResult(error_occurred=True, error_message=error_message)

                        number += remainder[pos]
                        pos += 1

                    # Return the result

                    constant_type = ConstantType.DOUBLE
                    argument_len = len(number)
                    remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                    return _ProcessingResult(constant_type=constant_type, text=number, remainder=remainder)

            else:
                constant_type = ConstantType.DOUBLE
                argument_len = len(number)
                remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                return _ProcessingResult(constant_type=constant_type, text=number, remainder=remainder)

        elif pos < remainder_len and (remainder[pos] == 'e' or remainder[pos] == 'E'):
            if remainder[pos - 1] == '_':
                error_message = "underscores cannot appear directly before an 'e' or 'E' in a number"
                return _ProcessingResult(error_occurred=True, error_message=error_message)

            number += remainder[pos]
            pos += 1

            # Check if we have a negative exponent

            if pos < remainder_len and remainder[pos] == '-':
                number += "-"
                pos += 1

            # Check that an integer appears after the 'e' or 'E' character

            if pos >= remainder_len:
                error_message = "scientific notation requires an integer to appear after the 'e' or 'E'"
                return _ProcessingResult(error_occurred=True, error_message=error_message)

            elif not str.isdigit(remainder[pos]):
                error_message = "scientific notation requires an integer to appear after the 'e' or 'E'"
                return _ProcessingResult(error_occurred=True, error_message=error_message)

            else:
                # Read in the exponent

                while pos < remainder_len and (str.isdigit(remainder[pos]) or remainder[pos] == '_'):
                    if remainder[pos] == '_':
                        number_len = len(number)
                        last_char = number[number_len - 1]

                        if not str.isdigit(last_char) and last_char != '_':
                            error_message = "underscores can only follow digits or underscores in numbers"
                            return _ProcessingResult(error_occurred=True, error_message=error_message)

                        elif pos == remainder_len - 1:
                            error_message = "numbers cannot end with an underscore"
                            return _ProcessingResult(error_occurred=True, error_message=error_message)

                    number += remainder[pos]
                    pos += 1

                # Return the result

                constant_type = ConstantType.DOUBLE
                argument_len = len(number)
                remainder = remainder[argument_len:] if argument_len < remainder_len else ""
                return _ProcessingResult(constant_type=constant_type, text=number, remainder=remainder)

        else:
            constant_type = ConstantType.INT
            argument_len = len(number)
            remainder = remainder[argument_len:] if argument_len < remainder_len else ""
            return _ProcessingResult(constant_type=constant_type, text=number, remainder=remainder)

    @staticmethod
    def _process_number_or_datetime_argument(remainder: str) -> _ProcessingResult:
        """
        Process a symbol that could either be a number or a date/time.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in the integer part

        number = ""
        remainder_len = len(remainder)
        found_underscore = False
        pos = 0

        while pos < remainder_len and (str.isdigit(remainder[pos]) or remainder[pos] == '_'):
            if remainder[pos] == '_':
                found_underscore = True

            number += remainder[pos]
            pos += 1

        # Date/times must started with 4 digits (the year) and a hyphen

        if pos < remainder_len and len(number) == 4 and remainder[pos] == '-' and not found_underscore:
            return LexicalParser._process_datetime(remainder)
        else:
            return LexicalParser._process_number_argument(remainder)

    @staticmethod
    def _process_single_quoted_str(remainder: str) -> _ProcessingResult:
        """
        Process a single quoted string symbol.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in until we see a closing double quote or come to the end

        text = "'"
        remainder_len = len(remainder)
        pos = 1

        while pos < remainder_len and remainder[pos] != "'":
            # Deal with any escaped single quotes

            if remainder[pos] == '\\' and pos < (remainder_len - 1) and remainder[pos + 1] == "'":
                text += "\\'"
                pos += 1
            else:
                text += remainder[pos]

            pos += 1

        # Check that we had a closing single quote

        if pos < remainder_len and remainder[pos] == "'":
            text += "'"
            argument = text
            argument_len = len(argument)
            remainder = remainder[argument_len] if argument_len < remainder_len else ""
            constant_type = ConstantType.STRING

            return _ProcessingResult(constant_type=constant_type, text=argument, remainder=remainder)

        else:
            error_message = "a string does not have a closing single quote (') character"
            return _ProcessingResult(error_occurred=True, error_message=error_message)

    @staticmethod
    def _process_double_quoted_str(remainder: str) -> _ProcessingResult:
        """
        Process a double quoted string symbol.

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        # Read in until we see a closing double quote or come to the end

        text = "\""
        remainder_len = len(remainder)
        pos = 1

        while pos < remainder_len and remainder[pos] != '"':
            # Deal with any escaped double quotes

            if remainder[pos] == '\\' and pos < (remainder_len - 1) and remainder[pos + 1] == '"':
                text += "\\\""
                pos += 1
            else:
                text += remainder[pos]

            pos += 1

        # Check that we had a closing double quote

        if pos < remainder_len and remainder[pos] == '"':
            text += '"'
            argument = text
            argument_len = len(argument)
            remainder = remainder[argument_len] if argument_len < remainder_len else ""
            constant_type = ConstantType.STRING

            return _ProcessingResult(constant_type=constant_type, text=argument, remainder=remainder)

        else:
            error_message = 'a string does not have a closing double quote (") character'
            return _ProcessingResult(error_occurred=True, error_message=error_message)

    @staticmethod
    def _process_boolean(boolean_str: str,
                         remainder: str) -> _ProcessingResult:
        """
        Process a Boolean symbol.

        :param boolean_str: The Boolean being processed.
        :type boolean_str: str

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        constant_type = ConstantType.BOOL
        argument = remainder[:len(boolean_str)]
        argument_len = len(argument)
        remainder_len = len(remainder)
        remainder = remainder[argument_len:] if argument_len < remainder_len else ""
        return _ProcessingResult(constant_type=constant_type, text=boolean_str, remainder=remainder)

    @staticmethod
    def _process_operator(operator_str: str,
                          remainder: str) -> _ProcessingResult:
        """
        Process an operator symbol.

        :param operator_str: The operator being processed.
        :type operator_str: str

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        operator_len = len(operator_str)
        remainder_len = len(remainder)
        remainder = remainder[operator_len:] if operator_len < remainder_len else ""
        return _ProcessingResult(text=operator_str, remainder=remainder)

    @staticmethod
    def _process_bracket(bracket_str: str,
                         remainder: str) -> _ProcessingResult:
        """
        Process a bracket symbol.

        :param bracket_str: The bracket being processed.
        :type bracket_str: str

        :param remainder: The remainder of the input.
        :type remainder: str

        :return: The result of processing remainder.
        :rtype: _ProcessingResult
        """
        bracket_len = len(bracket_str)
        remainder_len = len(remainder)
        remainder = remainder[bracket_len:] if bracket_len < remainder_len else ""
        return _ProcessingResult(text=bracket_str, remainder=remainder)

    @staticmethod
    def _starts_with(token: str,
                     remainder: str) -> bool:
        """
        Checks if a given piece of text starts with a provide token.

        :param token: The token that should be at the start of remainder.
        :type token: str

        :param remainder: The remainder of the input.
        :type token: str

        :return: True if remainder starts with token, False otherwise.
        :rtype: bool
        """
        if remainder.startswith(token):
            token_len = len(token)
            remainder_len = len(remainder)

            if token_len < remainder_len:
                return not str.isalpha(remainder[token_len])
            else:
                return True
        else:
            return False

    def get_next_symbol(self) -> Symbol or None:
        """
        Obtains the next symbol from the input.

        :return: The next symbol, or None if there are no symbols left.
        :rtype: Symbol or None
        """
        # Make sure there is anything left to process

        if self._remainder is None:
            return None

        else:
            remainder = self._remainder.strip()
            remainder_len = len(remainder)

            if remainder_len == 0:
                return None

            else:
                # Check what type of symbol we have

                remainder_lower = remainder.lower()

                if remainder[0] == "'":
                    result = LexicalParser._process_single_quoted_str(remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return StringConstant(result.text)

                elif remainder[0] == '"':
                    result = LexicalParser._process_double_quoted_str(remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return StringConstant(result.text)

                elif str.isdigit(remainder[0]):
                    result = LexicalParser._process_number_or_datetime_argument(remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder

                        if ConstantType.INT == result.constant_type:
                            value = int(result.text.replace("_", ""))
                            return IntegerConstant(result.text, value)

                        elif ConstantType.DOUBLE == result.constant_type:
                            value = float(result.text.replace("_", ""))
                            return DoubleConstant(result.text, value)

                        elif ConstantType.DATE_TIME == result.constant_type:
                            value = parse_timestamp_str(result.text)
                            return DateTimeConstant(result.text, value)

                        else:
                            raise ValueError("Unrecognised symbol")

                elif LexicalParser._starts_with(LexicalParser._TRUE_CONSTANT, remainder_lower):
                    result = LexicalParser._process_boolean(LexicalParser._TRUE_CONSTANT, remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return BooleanConstant(result.text, bool(result.text))

                elif LexicalParser._starts_with(LexicalParser._FALSE_CONSTANT, remainder_lower):
                    result = LexicalParser._process_boolean(LexicalParser._FALSE_CONSTANT, remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return BooleanConstant(result.text, bool(result.text))

                elif LexicalParser._starts_with(str(OperatorTypes.AND), remainder_lower):
                    operator_type = OperatorTypes.AND
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return LogicalOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.OR), remainder_lower):
                    operator_type = OperatorTypes.OR
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return LogicalOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.NOT), remainder_lower):
                    operator_type = OperatorTypes.NOT
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return LogicalOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.LESS_THAN_OR_EQUALS), remainder_lower):
                    operator_type = OperatorTypes.LESS_THAN_OR_EQUALS
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.LESS_THAN), remainder_lower):
                    operator_type = OperatorTypes.LESS_THAN
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.GREATER_THAN_OR_EQUALS), remainder_lower):
                    operator_type = OperatorTypes.GREATER_THAN_OR_EQUALS
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.GREATER_THAN), remainder_lower):
                    operator_type = OperatorTypes.GREATER_THAN
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.NOT_EQUALS), remainder_lower):
                    operator_type = OperatorTypes.NOT_EQUALS
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.EQUALS), remainder_lower):
                    operator_type = OperatorTypes.EQUALS
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.UNLIKE), remainder_lower):
                    operator_type = OperatorTypes.UNLIKE
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif LexicalParser._starts_with(str(OperatorTypes.LIKE), remainder_lower):
                    operator_type = OperatorTypes.LIKE
                    result = LexicalParser._process_operator(str(operator_type), remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return ComparisonOperator(result.text, operator_type)

                elif remainder_lower.startswith(LexicalParser._LEFT_BRACKET):
                    result = LexicalParser._process_bracket(LexicalParser._LEFT_BRACKET, remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return LeftBracket()

                elif remainder_lower.startswith(LexicalParser._RIGHT_BRACKET):
                    result = LexicalParser._process_bracket(LexicalParser._RIGHT_BRACKET, remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return RightBracket()

                elif str.isalpha(remainder_lower[0]):
                    result = LexicalParser._process_feature_reference(remainder)

                    if result.error_occurred:
                        raise ValueError(result.error_message)
                    else:
                        self._remainder = result.remainder
                        return FeatureReference(result.text)

                else:
                    raise ValueError(f"unrecognised symbol '{self._remainder}'")


class FilterParser:
    """
    Used to parse a filter.
    """
    _OPERATOR_ARGUMENT_TYPES = {OperatorTypes.EQUALS: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.STRING, ConstantType.DATE_TIME, ConstantType.BOOL, ConstantType.FEATURE},
                                OperatorTypes.NOT_EQUALS: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.STRING, ConstantType.DATE_TIME, ConstantType.BOOL, ConstantType.FEATURE},
                                OperatorTypes.GREATER_THAN: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.DATE_TIME, ConstantType.FEATURE},
                                OperatorTypes.GREATER_THAN_OR_EQUALS: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.DATE_TIME, ConstantType.FEATURE},
                                OperatorTypes.LESS_THAN: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.DATE_TIME, ConstantType.FEATURE},
                                OperatorTypes.LESS_THAN_OR_EQUALS: {ConstantType.DOUBLE, ConstantType.INT, ConstantType.DATE_TIME, ConstantType.FEATURE},
                                OperatorTypes.LIKE: {ConstantType.STRING},
                                OperatorTypes.UNLIKE: {ConstantType.STRING}}

    def __init__(self,
                 filter_expr: str):
        """
        :param filter_expr: The filter to parse.
        :type filter_expr: str
        """
        self._lexicalParser = LexicalParser(filter_expr)
        self._symbol = self._lexicalParser.get_next_symbol()
        self._expression_stack = list()

    def build(self) -> BooleanExpression:
        """
        Build a Boolean expression from the input given.

        :return: A Boolean expression representing the input given in the constructor.
        :rtype: BooleanExpression
        """
        self._boolean_expression()

        if self._symbol is not None or len(self._expression_stack) != 1:
            raise ValueError("no valid Boolean expression was found")
        else:
            return self._expression_stack.pop()

    def _next_symbol(self):
        """
        Moves the lexical parser to the next symbol.
        """
        self._symbol = self._lexicalParser.get_next_symbol()

    def _boolean_expression(self):
        """
        Parses a Boolean expression.
        """
        self._boolean_term()

        while isinstance(self._symbol, LogicalOperator) and OperatorTypes.OR == self._symbol.operator_type():
            if len(self._expression_stack) > 0:
                left = self._expression_stack.pop()
                or_symbol = self._symbol

                self._next_symbol()
                self._boolean_term()

                if len(self._expression_stack) > 0:
                    self._expression_stack.append(OrExpression(left, or_symbol, self._expression_stack.pop()))
                else:
                    raise ValueError("the OR operator must be followed by a Boolean expression")
            else:
                raise ValueError("a Boolean expression was expected after the OR operator")

    def _boolean_term(self):
        """
        Parses a Boolean term.
        """
        self._boolean_factor()

        while isinstance(self._symbol, LogicalOperator) and OperatorTypes.AND == self._symbol.operator_type():
            if len(self._expression_stack) > 0:
                left = self._expression_stack.pop()
                and_symbol = self._symbol

                self._next_symbol()
                self._boolean_factor()

                if len(self._expression_stack) > 0:
                    self._expression_stack.append(AndExpression(left, and_symbol, self._expression_stack.pop()))
                else:
                    raise ValueError("the AND operator must be followed by a Boolean expression")
            else:
                raise ValueError("a Boolean expression was expected after the AND operator")

    def _comparison_expression(self):
        """
        Parses a comparison expression.
        """
        if isinstance(self._symbol, ComparisonOperator):
            operator = self._symbol
            operator_type = operator.operator_type()

            if OperatorTypes.EQUALS == operator_type or OperatorTypes.NOT_EQUALS == operator_type or \
                    OperatorTypes.GREATER_THAN_OR_EQUALS == operator_type or OperatorTypes.GREATER_THAN == operator_type or \
                    OperatorTypes.LESS_THAN_OR_EQUALS == operator_type or OperatorTypes.LESS_THAN == operator_type or \
                    OperatorTypes.LIKE == operator_type or OperatorTypes.UNLIKE == operator_type:
                self._next_symbol()

                if isinstance(self._symbol, Constant):
                    constant = self._symbol

                    if operator_type in FilterParser._OPERATOR_ARGUMENT_TYPES and constant.constant_type() in FilterParser._OPERATOR_ARGUMENT_TYPES[operator_type]:
                        self._next_symbol()
                        comparison_operator = ComparisonOperator(str(operator), operator.operator_type())
                        self._expression_stack.append(ComparisonExpression(comparison_operator, constant))

                    else:
                        if isinstance(constant, FeatureReference):
                            raise ValueError(f"the operator \"{operator}\" cannot be used with the feature reference '{constant}'")

                        else:
                            raise ValueError(f"the operator \"{operator}\" cannot be used with the constant '{constant}'")

                else:
                    raise ValueError(f"a constant or feature reference is expected after the operator '{operator}'")

            else:
                raise ValueError(f"an unexpected comparison operator '{operator}' was found")

        else:
            raise ValueError("a comparison operator was expected but none was found")

    def _boolean_factor(self):
        """
        Parses a Boolean factor.
        """
        if self._symbol is not None:
            if isinstance(self._symbol, ComparisonOperator):
                self._comparison_expression()

            elif isinstance(self._symbol, LogicalOperator) and OperatorTypes.NOT == self._symbol.operator_type():
                not_symbol = self._symbol
                self._next_symbol()
                self._boolean_factor()

                if len(self._expression_stack) > 0:
                    self._expression_stack.append(NotExpression(not_symbol, self._expression_stack.pop()))
                else:
                    raise ValueError("the NOT operator must negate a Boolean expression")

            elif isinstance(self._symbol, LeftBracket):
                self._next_symbol()
                self._boolean_expression()

                if len(self._expression_stack) > 0 and isinstance(self._symbol, RightBracket):
                    self._next_symbol()
                else:
                    raise ValueError("the NOT operator must negate a Boolean expression")
            else:
                raise ValueError("unable to find a valid comparison operator")


def is_valid_feature(feature: str) -> bool:
    """
    Determines if a reference to a feature if of a valid format.

    :param feature The feature to be evaluated.
    :type feature: str

    :return: True if the feature is valid, false otherwise.
    :rtype: bool
    """
    try:
        lexical_parser = LexicalParser(feature)
        feature_symbol = lexical_parser.get_next_symbol()
        next_symbol = lexical_parser.get_next_symbol()
        return isinstance(feature_symbol, FeatureReference) and next_symbol is None
    except:
        return False


def is_valid_filter(filter_expr: str) -> str or None:
    """
    Evaluates if a filter is valid or not.

    :param filter_expr The filter to evaluate.
    :type filter_expr: str

    :return: If invalid then an error message is returned, None otherwise.
    :rtype: str or None
    """
    if filter is None:
        return None
    else:
        try:
            FilterParser(filter_expr).build()
            return None
        except ValueError as ve:
            return str(ve)


def parse_filter(filter_expr: str) -> BooleanExpression:
    """
    Parses a filter; assumes is_valid_filter(filter).

    :param filter_expr The filter to parse.
    :type filter_expr: str

    :return: The result of parsing the filter.
    :rtype: BooleanExpression
    """
    return FilterParser(filter_expr).build()
