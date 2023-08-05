# -*- coding: utf-8 -*-
import functools

CACHE_RETURN_DICT = dict()


def cache_return(func):
    @functools.wraps(func)
    def wrapper_cache_return(*args, **kwargs):
        global CACHE_RETURN_DICT
        if func in CACHE_RETURN_DICT:
            return CACHE_RETURN_DICT[func]
        rv = func(*args, **kwargs)
        CACHE_RETURN_DICT[func] = rv
        return rv

    return wrapper_cache_return
