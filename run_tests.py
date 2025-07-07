#!/usr/bin/env python3
"""
Test runner script for the models.py unit tests.

This script provides an easy way to run the tests with proper setup.
"""
import sys
import subprocess

def run_tests():
    """Run the pytest tests with appropriate options."""
    try:
        # Run pytest with verbose output and coverage if available
        cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]
        
        print("Running tests for src/models.py...")
        print("=" * 50)
        
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("All tests passed! ✓")
        else:
            print("\n" + "=" * 50)
            print("Some tests failed. ✗")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()