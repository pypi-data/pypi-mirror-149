# -*- coding: UTF-8 -*-  
from __future__ import unicode_literals
from functools import wraps
import os



def db_config_vars(f):
    """
    Replacing step parameters with feature's variable values if they
    set in feature (start with a "$").
    """
    @wraps(f)
    def wrapper(context, **kwargs):
        decoded_kwargs = {}
        for key, value in kwargs.items():
            if str(value).startswith('$'):
                value = context.db_config[value.replace('$','')]
            decoded_kwargs[key] = value
        return f(context, **decoded_kwargs)
    return wrapper

