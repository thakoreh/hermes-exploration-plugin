"""Hermes directory-plugin entry point (also available as a pip entry point)."""

if __package__:
    from .hermes_exploration import register
else:  # Direct source import (for example pytest collection in a hyphenated clone).
    from hermes_exploration import register

__all__ = ["register"]
