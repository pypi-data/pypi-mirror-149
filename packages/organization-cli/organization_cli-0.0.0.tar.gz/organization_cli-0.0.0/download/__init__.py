# -*- coding: utf-8 -*-
"""Namespace-only module."""
from main import download
from main import TestApp


# This line must appear in the __init__.py for all namespace packages
__path__ = __import__('pkgutil').extend_path(__path__, __name__)