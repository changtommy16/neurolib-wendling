"""
Helper script to copy wendling module and tutorial into the package structure
Run this script to set up the package before installation
"""

import shutil
from pathlib import Path

# Define paths
SCRIPT_DIR = Path(__file__).parent
WENDLING_SOURCE = Path(r"c:\Epilepsy_project\Neurolib_desktop\Neurolib_package\neurolib\models\wendling")
TUTORIAL_SOURCE = Path(r"c:\Epilepsy_project\whole_brain_wendling\Validation_for_single_node\Wendling_Tutorial_Clean.ipynb")

WENDLING_DEST = SCRIPT_DIR / "neurolib_wendling" / "models" / "wendling"
TUTORIAL_DEST = SCRIPT_DIR / "tutorials"

def copy_wendling_module():
    """Copy wendling module to package structure"""
    print("📦 Copying Wendling module...")
    
    if WENDLING_DEST.exists():
        print(f"   Removing existing: {WENDLING_DEST}")
        shutil.rmtree(WENDLING_DEST)
    
    print(f"   Source: {WENDLING_SOURCE}")
    print(f"   Destination: {WENDLING_DEST}")
    shutil.copytree(WENDLING_SOURCE, WENDLING_DEST)
    print("   ✓ Wendling module copied")

def copy_tutorial():
    """Copy tutorial notebook to package"""
    print("\n📓 Copying tutorial notebook...")
    
    TUTORIAL_DEST.mkdir(parents=True, exist_ok=True)
    
    dest_file = TUTORIAL_DEST / "Wendling_Tutorial_Clean.ipynb"
    print(f"   Source: {TUTORIAL_SOURCE}")
    print(f"   Destination: {dest_file}")
    shutil.copy2(TUTORIAL_SOURCE, dest_file)
    print("   ✓ Tutorial copied")

def verify_structure():
    """Verify the package structure is correct"""
    print("\n🔍 Verifying package structure...")
    
    required_files = [
        "setup.py",
        "README.md",
        "requirements.txt",
        "neurolib_wendling/__init__.py",
        "neurolib_wendling/models/__init__.py",
        "neurolib_wendling/models/wendling/__init__.py",
        "neurolib_wendling/models/wendling/model.py",
        "tutorials/Wendling_Tutorial_Clean.ipynb",
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = SCRIPT_DIR / file_path
        if full_path.exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} - MISSING!")
            all_good = False
    
    if all_good:
        print("\n✅ Package structure is complete!")
        print("\nNext steps:")
        print("1. Edit setup.py to add your name and email")
        print("2. Test installation:")
        print("   cd neurolib-wendling-package")
        print("   pip install -e .")
        print("3. Test import:")
        print("   python -c 'from neurolib_wendling.models.wendling import WendlingModel'")
    else:
        print("\n❌ Package structure is incomplete. Please fix missing files.")
    
    return all_good

def main():
    print("=" * 60)
    print("neurolib-wendling Package Setup")
    print("=" * 60)
    
    try:
        # Check if source files exist
        if not WENDLING_SOURCE.exists():
            print(f"❌ Error: Wendling source not found at {WENDLING_SOURCE}")
            return
        
        if not TUTORIAL_SOURCE.exists():
            print(f"❌ Error: Tutorial source not found at {TUTORIAL_SOURCE}")
            return
        
        # Copy files
        copy_wendling_module()
        copy_tutorial()
        
        # Verify structure
        verify_structure()
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        raise

if __name__ == "__main__":
    main()
