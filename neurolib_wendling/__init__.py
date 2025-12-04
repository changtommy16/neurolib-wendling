"""
neurolib-wendling: Wendling model extension for neurolib
"""

__version__ = "0.1.0"

# Auto-register to neurolib.models namespace
# This allows: from neurolib.models.wendling import WendlingModel
try:
    from . import register
except ImportError:
    pass

# Import main model for convenience
# Lazy import to avoid circular dependencies
def __getattr__(name):
    if name == 'WendlingModel':
        from .models.wendling import WendlingModel
        return WendlingModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['WendlingModel', '__version__']
