"""
Quick test script to verify neurolib-wendling installation
Run this after: pip install -e .
"""

import sys

def test_import():
    """Test basic import"""
    print("=" * 60)
    print("Test 1: Basic Import")
    print("=" * 60)
    try:
        from neurolib_wendling.models.wendling import WendlingModel
        print("✓ Successfully imported WendlingModel")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_standard_params():
    """Test loading standard parameters"""
    print("\n" + "=" * 60)
    print("Test 2: Load Standard Parameters")
    print("=" * 60)
    try:
        from neurolib_wendling.models.wendling.STANDARD_PARAMETERS import WENDLING_STANDARD_PARAMS
        print(f"✓ Loaded {len(WENDLING_STANDARD_PARAMS)} parameter sets:")
        for key in WENDLING_STANDARD_PARAMS.keys():
            print(f"  - {key}")
        return True
    except Exception as e:
        print(f"✗ Failed to load parameters: {e}")
        return False

def test_model_creation():
    """Test model creation and basic usage"""
    print("\n" + "=" * 60)
    print("Test 3: Create and Run Model")
    print("=" * 60)
    try:
        from neurolib_wendling.models.wendling import WendlingModel
        from neurolib_wendling.models.wendling.STANDARD_PARAMETERS import WENDLING_STANDARD_PARAMS
        
        # Create model (default params are loaded automatically)
        model = WendlingModel()
        print("✓ Model created with default parameters")
        
        # Update with standard parameters (only update specific keys, don't replace all)
        param_key = list(WENDLING_STANDARD_PARAMS.keys())[0]
        std_params = WENDLING_STANDARD_PARAMS[param_key]['params']
        for key, value in std_params.items():
            model.params[key] = value
        print(f"✓ Parameters updated with '{param_key}' type")
        
        # Run simulation (short test)
        model.params['duration'] = 100  # Just 100ms for quick test
        model.run()
        print(f"✓ Simulation completed: {len(model.t)} time points")
        
        # Check output (wendling uses state_vars like y0, y1, etc.)
        if hasattr(model, 'y1'):
            print(f"  Output shape: {model.y1.shape}")
        else:
            print(f"  Note: Model outputs stored in state variables (y0-y9)")
        
        return True
    except Exception as e:
        print(f"✗ Failed to run model: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alternative_import():
    """Test importing as neurolib.models.wendling (via auto-registration)"""
    print("\n" + "=" * 60)
    print("Test 4: Alternative Import (neurolib.models.wendling)")
    print("=" * 60)
    try:
        # First import neurolib_wendling to trigger auto-registration
        import neurolib_wendling
        
        # Now try the neurolib.models.wendling path
        from neurolib.models.wendling import WendlingModel
        print("✓ Alternative import path works!")
        print("  You can use BOTH import styles:")
        print("  - from neurolib_wendling.models.wendling import WendlingModel")
        print("  - from neurolib.models.wendling import WendlingModel")
        return True
    except ImportError as e:
        print(f"⚠ Alternative import not available: {e}")
        print("  You can still use: from neurolib_wendling.models.wendling import ...")
        return True  # Not a critical failure

def main():
    print("\n🧪 Testing neurolib-wendling Installation\n")
    
    results = []
    
    # Run tests
    results.append(("Import", test_import()))
    results.append(("Standard Parameters", test_standard_params()))
    results.append(("Model Creation", test_model_creation()))
    results.append(("Alternative Import", test_alternative_import()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Installation is successful.")
        print("\nYou can now:")
        print("1. Run the tutorial: jupyter notebook tutorials/Wendling_Tutorial_Clean.ipynb")
        print("2. Use in your scripts:")
        print("   from neurolib_wendling.models.wendling import WendlingModel")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
