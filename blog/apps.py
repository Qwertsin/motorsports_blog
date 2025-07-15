"""App configuration for the blog app."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Default config for the blog app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
