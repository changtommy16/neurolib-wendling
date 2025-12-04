"""
Auto-registration module to make wendling available under neurolib.models namespace
"""

import sys
from types import ModuleType


def register_wendling_to_neurolib():
    """
    Register wendling model to neurolib.models namespace.
    
    After calling this, you can use:
        from neurolib.models.wendling import WendlingModel
    
    This is a "monkey patch" approach to make the extension feel native.
    """
    try:
        import neurolib.models
        from neurolib_wendling.models import wendling
        
        # Register wendling as a submodule of neurolib.models
        sys.modules['neurolib.models.wendling'] = wendling
        
        # Also add to neurolib.models as an attribute for direct access
        setattr(neurolib.models, 'wendling', wendling)
        
        return True
    except ImportError as e:
        print(f"Warning: Could not register wendling to neurolib namespace: {e}")
        return False


# Auto-register on import
_registered = register_wendling_to_neurolib()

if _registered:
    __all__ = ['register_wendling_to_neurolib']
else:
    __all__ = []
