# -*- coding: UTF-8 -*-  
from __future__ import unicode_literals
from functools import wraps
import jinja2
import os


def _get_data_from_context(context):
    """Use context.text as a template and render against any stored state."""
    data = context.text if context.text else ''
    # Always clear the text to avoid accidental re-use.
    context.text = ''
    # NB rendering the template always returns unicode.
    result = jinja2.Template(data).render(context.db_config)
    return result.encode('utf8')


def db_config_vars(f):
    """Decorator to dereference step parameters and data.

    This involves three steps:

        1) Rendering feature file step parameters as a Jinja2 template against
        context.db_config.

        2) Replacing step parameters with environment variable values if they
        look like an environment variable (start with a "$").

        3) Treating context.text as a Jinja2 template rendered against
        context.db_config, and putting the result in context.data.

    """
    @wraps(f)
    def wrapper(context, **kwargs):
        decoded_kwargs = {}
        for key, value in kwargs.items():
            value = jinja2.Template(value).render(context.db_config)
            if value.startswith('$'):
                value = os.environ.get(value[1:], '')
            decoded_kwargs[key] = value
        context.data = _get_data_from_context(context)
        return f(context, **decoded_kwargs)
    return wrapper

