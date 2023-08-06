import re


from functools import partial
from dataclasses import dataclass
from typing import Tuple, Callable, Union

from jsonpath_ng import jsonpath, parse as jsonpath_parse

from .exceptions import NotifierException

RULE_PARSER = re.compile("(.*?)([\s]+)([=<>!]+)([\s]+)(.*)")
REGEX_SPACE = re.compile("\s\s+")
REGEX_BOOL_TRUE = re.compile("[tT][rR][uU][eE]")
REGEX_BOOL_FALSE = re.compile("[fF][aA][lL][sS][eE]")
REGEX_FLOAT = re.compile("[\d]+\.[\d]+")
REGEX_INT = re.compile("[\d]+")
VALID_OPERATIONS = {
    "==": lambda x, y: x == y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "!=": lambda x, y: x != y,
}


@dataclass
class CompiledRule:
    left: Callable = None
    operation: Callable = None
    right: Callable = None

    def match(self, text: str) -> bool:
        if not self.left:
            return True

        left = self.left(text)
        right = self.right(text)

        if left and right:
            return self.operation(left, right)

        else:
            return False

def _make_rules_(rule_text: str) -> Tuple[Callable, Callable, Callable]:

    def __clean__text__(text: str) -> str:

        if text.startswith(("'", '"')):
            start = 1
        else:
            start = 0

        if text.endswith(("'", '"')):
            end = -1
        else:
            end = len(text) - 1

        return text[start:end]

    def __resolve__(text):

        # Check right values
        if REGEX_BOOL_TRUE.match(text):
            ret = lambda x: True

        elif REGEX_BOOL_FALSE.match(text):
            ret = lambda x: False

        elif REGEX_FLOAT.match(text):
            ret = lambda x: float(text_right)

        elif REGEX_INT.match(text):
            ret = lambda x: int(text_right)

        elif text.startswith(('"', '"')):

            new_text = __clean__text__(text)

            ret = lambda x: new_text

        elif "." in text and " " not in text:  # a Json path

            try:
                p = jsonpath_parse(text)
            except:

                new_text = __clean__text__(text)

                ret = lambda x: new_text

            else:

                def _extract_data_(json_parse, input_json: dict):
                    if f := json_parse.find(input_json):
                        return f[0].value
                    else:
                        return None

                ret = partial(_extract_data_, p)

        else:
            new_text = __clean__text__(text)

            ret = lambda x: new_text

        return ret

    # -------------------------------------------------------------------------
    # Start function
    # -------------------------------------------------------------------------

    # remove duplicated spaces
    rule_text = REGEX_SPACE.sub(' ', rule_text)

    if found := RULE_PARSER.match(rule_text):
        text_left, _, comparison, _, text_right =  found.groups()
    else:
        raise NotifierException("Invalid rule format")

    # Check comparison symbols
    comparison = comparison.strip()

    if not any(comparison in c for c in ("==", ">=", ">", "<", "<=", "!=")):
        raise NotifierException("Invalid comparison operator")

    operation = VALID_OPERATIONS[comparison]

    # Prepare JSONPath expression
    # left = jsonpath_parse(text_left)
    left = __resolve__(text_left)
    right = __resolve__(text_right)

    return left, operation, right

def compile_rule(rule_text: str) -> CompiledRule or NotifierException:
    if not rule_text:
        return None

    left, operation, right = _make_rules_(rule_text)

    return CompiledRule(
        left=left,
        operation=operation,
        right=right
    )



__all__ = ("compile_rule", )
