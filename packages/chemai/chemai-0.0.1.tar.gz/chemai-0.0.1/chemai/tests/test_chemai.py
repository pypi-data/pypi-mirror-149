"""
Unit and regression test for the chemai package.
"""

# Import package, test suite, and other packages as needed
import chemai
import pytest
import sys

def test_chemai_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "chemai" in sys.modules
