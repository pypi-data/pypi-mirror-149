import pytest
from django.core.exceptions import ValidationError

from medux_online.plugins.prescriptions.models import validate_svnr


def test_anumeric_svnr1():
    with pytest.raises(ValidationError):
        validate_svnr("123456789o")


def test_anumeric_svnr2():
    with pytest.raises(ValidationError):
        validate_svnr("kjsafdhg")


def test_svnr_wrong_len_tooshort():
    with pytest.raises(ValidationError):
        validate_svnr("123456789")


def test_svnr_len_toolong():
    with pytest.raises(ValidationError):
        validate_svnr("12345678901")


def test_svnr_startswith0():
    with pytest.raises(ValidationError):
        validate_svnr("0123456789")


def test_svnr_check_number():
    for i in [1, 2, 3, 4, 6, 7, 8, 9, 0]:
        with pytest.raises(ValidationError):
            validate_svnr(f"123{i}010101")


def test_svnr_day_wrong():
    with pytest.raises(ValidationError):
        validate_svnr("2635321173")  # day=32
