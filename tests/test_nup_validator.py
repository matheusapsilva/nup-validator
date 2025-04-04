import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nup_validator import validate_nup

def test_valid_nup():
    assert validate_nup("12345.678901/2023-94")
    assert validate_nup("35041.000387/2000-19")

def test_sn_case():
    assert validate_nup("S/N")

def test_invalid_format():
    assert not validate_nup("12345678901202342")
    assert not validate_nup("12345-678901/2023-42")

def test_invalid_dv():
    assert not validate_nup("12345.678901/2023-99")

def test_missing_separators():
    assert not validate_nup("12345678901")

def test_short_prefix():
    assert not validate_nup("123.678901/2023-42")
