"""Core module for dependency injection and application setup."""

from .container import ServiceContainer, get_container

__all__ = ['ServiceContainer', 'get_container']
