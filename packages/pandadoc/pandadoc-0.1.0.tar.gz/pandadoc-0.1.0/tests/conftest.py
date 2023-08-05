import pytest
from pandadoc import call_pandoc


@pytest.fixture(scope="session")
def pandoc_input_formats():
    input_formats_str = call_pandoc(["--list-input-formats"])
    input_formats = [
        format for format in input_formats_str.split(sep="\n") if format != ""
    ]
    return input_formats


@pytest.fixture(scope="session")
def pandoc_output_formats():
    output_formats_str = call_pandoc(["--list-output-formats"])
    output_formats = [
        format for format in output_formats_str.split(sep="\n") if format != ""
    ]
    return output_formats
