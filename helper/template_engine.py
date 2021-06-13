# Module name : TEngine.py
# re-created by alvifsandanamahardika at 6/11/21

import re
from enum import Enum


class Delimiter(Enum):
    RAW_LEFT_DELIMITER = r'<\%'
    RAW_RIGHT_DELIMITER = r'%\>'
    LEFT_DELIMITER = '<%'
    RIGHT_DELIMITER = '%>'
    PATTERN = r'<%(.*?)%>'


class TEngine(object):
    """
    Process the given template text that has delimiters
    in the form of <% code_here %>
    """

    def __init__(self, text):
        # delimiter with regExp flag
        self.delimiter = re.compile(Delimiter.PATTERN.value, re.DOTALL)
        # tokens
        self.tokens = self.compile(text)

    def compile(self, template_string):
        """
        Compile the given string to template function and
        store it to the list.
        :param template_string: String
        :return: tokens: list of token
        """
        # list for storing produced token from the given string
        tokens = []
        # iterate and detect the code block inside the string
        for idx, token in enumerate(self.delimiter.split(template_string)):
            if idx % 2 == 0:
                # detected not a code block, add it to tokens[]
                if token:
                    tokens.append((
                        False,
                        token.replace(
                            Delimiter.RAW_RIGHT_DELIMITER.value,
                            Delimiter.RIGHT_DELIMITER.value).replace(
                            Delimiter.RAW_LEFT_DELIMITER.value, Delimiter.LEFT_DELIMITER.value)
                    ))
            else:
                # code block detected
                # find line
                lines = token.replace(Delimiter.RAW_LEFT_DELIMITER.value, Delimiter.LEFT_DELIMITER.value) \
                    .replace(Delimiter.RAW_RIGHT_DELIMITER.value, Delimiter.RIGHT_DELIMITER.value).splitlines()
                # find the indentation
                indent = min([len(line) - len(line.lstrip()) for line in lines if line.strip()])
                # realigned token
                realigned = '\n'.join(ln[indent:] for ln in lines)
                # add realigned token to the tokens[]
                tokens.append((True, compile(realigned, f'<template> {realigned[:20]}', 'exec')))
        return tokens

    def render(self, context=None, **kwargs):
        """
        Render the template according to the given context.

        :return: String
        """
        # store the given context
        global_context = {}
        # store the result
        result = []
        # group the given context or kwargs
        if context:
            global_context.update(context)
        elif kwargs:
            global_context.update(kwargs)

        # this function to output from context
        # to the rendered template
        def write(*args):
            result.extend([str(arg) for arg in args])

        def fmt_write(fmt, *args):
            result.append(fmt % args)

        # add write and fmt_write into global_context
        global_context['write'] = write
        global_context['fmt_write'] = fmt_write
        # run the code
        for is_code, token in self.tokens:
            if is_code:
                exec(token, global_context)
            else:
                result.append(token)
        return ''.join(result)

    __call__ = render
