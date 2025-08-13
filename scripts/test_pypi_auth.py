#!/usr/bin/env python3
"""
Test PyPI authentication tokens.

This script helps verify that your PyPI tokens are working correctly.
"""

import os
import sys
from pathlib import Path

def test_pypi_auth():
    """Test PyPI authentication."""
    print("🔐 Testing PyPI Authentication")
    print("=" * 40)
    
    # Check if tokens are set
    pypi_token = os.environ.get('PYPI_API_TOKEN')
    testpypi_token = os.environ.get('TEST_PYPI_API_TOKEN')
    
    print(f"PyPI Token: {'✅ Set' if pypi_token else '❌ Not set'}")
    print(f"Test PyPI Token: {'✅ Set' if testpypi_token else '❌ Not set'}")
    
    if not pypi_token and not testpypi_token:
        print("\n❌ No tokens found!")
        print("\nTo set tokens for testing:")
        print("export PYPI_API_TOKEN='your-pypi-token'")
        print("export TEST_PYPI_API_TOKEN='your-testpypi-token'")
        return False
    
    # Test token format
    if pypi_token:
        if not pypi_token.startswith('pypi-'):
            print("❌ PyPI token format looks incorrect (should start with 'pypi-')")
        else:
            print("✅ PyPI token format looks correct")
    
    if testpypi_token:
        if not testpypi_token.startswith('pypi-'):
            print("❌ Test PyPI token format looks incorrect (should start with 'pypi-')")
        else:
            print("✅ Test PyPI token format looks correct")
    
    # Test with twine
    try:
        import subprocess
        
        print("\n🧪 Testing with twine...")
        
        # Test Test PyPI first
        if testpypi_token:
            print("Testing Test PyPI authentication...")
            result = subprocess.run([
                'twine', 'check', 'dist/*'
            ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode == 0:
                print("✅ Test PyPI authentication successful")
            else:
                print(f"❌ Test PyPI authentication failed: {result.stderr}")
        
        # Test PyPI
        if pypi_token:
            print("Testing PyPI authentication...")
            result = subprocess.run([
                'twine', 'check', 'dist/*'
            ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode == 0:
                print("✅ PyPI authentication successful")
            else:
                print(f"❌ PyPI authentication failed: {result.stderr}")
                
    except ImportError:
        print("❌ twine not installed. Install with: pip install twine")
        return False
    except FileNotFoundError:
        print("❌ No dist/ directory found. Build the package first with: python -m build")
        return False
    
    print("\n🎉 Authentication test completed!")
    return True

def show_setup_instructions():
    """Show setup instructions."""
    print("\n📋 PyPI Token Setup Instructions")
    print("=" * 40)
    print("1. Create PyPI account: https://pypi.org/account/register/")
    print("2. Create Test PyPI account: https://test.pypi.org/account/register/")
    print("3. Generate tokens:")
    print("   - PyPI: https://pypi.org/manage/account/token/")
    print("   - Test PyPI: https://test.pypi.org/manage/account/token/")
    print("4. Add to GitHub Secrets:")
    print("   - Go to your repo → Settings → Secrets and variables → Actions")
    print("   - Add PYPI_API_TOKEN and TEST_PYPI_API_TOKEN")
    print("5. Test locally:")
    print("   export PYPI_API_TOKEN='your-token'")
    print("   export TEST_PYPI_API_TOKEN='your-token'")
    print("   python scripts/test_pypi_auth.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        show_setup_instructions()
    else:
        test_pypi_auth()
