"""Vercel entrypoint for the Django application."""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

from my_project.wsgi import application

__all__ = ["application"]
