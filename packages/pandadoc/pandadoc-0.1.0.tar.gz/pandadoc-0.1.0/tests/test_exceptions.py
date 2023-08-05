import pytest
from pandadoc.exceptions import (
    PandocBibliographyError,
    PandocError,
    PandocIOError,
    get_exception_by_error_code,
)


@pytest.mark.parametrize(
    "error_code,exception",
    [(1, PandocIOError), (25, PandocBibliographyError), (None, PandocError)],
)
def test_gets_correct_exception_for_valid_error_code(error_code, exception):
    exc = get_exception_by_error_code(error_code)
    assert exc == exception


@pytest.mark.parametrize("error_code", [-1, 123, 85])
def test_raises_value_error_for_nonexistent_error_code(error_code):
    with pytest.raises(ValueError):
        get_exception_by_error_code(error_code)
