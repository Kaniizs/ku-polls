"""This module contains an application named polls."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Config an application named polls."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
