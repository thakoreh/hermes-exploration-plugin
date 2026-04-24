"""
Hermes Exploration Plugin
Discover new tools, APIs, and models proactively.
"""

from .plugin import ExplorationPlugin
from .schemas import DiscoverySchema

__all__ = ["ExplorationPlugin", "DiscoverySchema"]
__version__ = "0.1.0"
