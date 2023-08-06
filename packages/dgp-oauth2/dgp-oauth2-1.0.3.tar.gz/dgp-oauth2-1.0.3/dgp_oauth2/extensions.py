from importlib import import_module

import logging

from .credentials import installed_extensions

installed_modules = [
    import_module(module_name)
    for module_name in installed_extensions
]


def on_new_user(user_info={}):
    for module in installed_modules:
        try:
            module.on_new_user(user_info)
        except AttributeError:
            pass


def on_user_login(user_info={}):
    for module in installed_modules:
        try:
            module.on_user_login(user_info)
        except AttributeError:
            pass


def on_user_logout(user_info={}):
    for module in installed_modules:
        try:
            module.on_user_logout(user_info)
        except AttributeError:
            pass
