import os.path
import tempfile

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings
from pandadoc import call_pandoc
from pandadoc.exceptions import (
    PandocError,
    PandocHttpError,
    PandocIOError,
    PandocPDFProgramNotFoundError,
    PandocUnknownReaderError,
    PandocUnknownWriterError,
)

from constants import BINARY_OUTPUT_FORMATS, EXAMPLE_DOCUMENTS, TEXT_OUTPUT_FORMATS


@settings(deadline=None)
@given(
    output_format=st.sampled_from(BINARY_OUTPUT_FORMATS + TEXT_OUTPUT_FORMATS),
    sample_input=st.sampled_from(EXAMPLE_DOCUMENTS),
)
def test_output_to_file(
    output_format, sample_input, pandoc_input_formats, pandoc_output_formats
):
    # Arrange
    input_format = sample_input["format"]
    input_text = sample_input["text"]
    options = ["-f", input_format, "-t", output_format]

    try:

        with tempfile.TemporaryDirectory() as temp_path:
            path_to_file = os.path.join(temp_path, "output.html")
            options.extend(["-o", path_to_file])

            # Act
            call_pandoc(options=options, input_text=input_text)

            # Assert
            assert os.path.isfile(path_to_file)
    except PandocUnknownReaderError:
        if input_format in pandoc_input_formats:
            raise
        pass
    except PandocUnknownWriterError:
        if output_format not in pandoc_output_formats:
            raise
        pass
    except (PandocPDFProgramNotFoundError, PandocIOError):
        pytest.xfail("No PDF program found.")
    except PandocError:
        pytest.fail("PandocError raised during conversion.")


@given(
    output_format=st.sampled_from(TEXT_OUTPUT_FORMATS),
    sample_input=st.sampled_from(EXAMPLE_DOCUMENTS),
)
def test_output_to_string(
    output_format, sample_input, pandoc_input_formats, pandoc_output_formats
):
    # Arrange
    input_format = sample_input["format"]
    input_text = sample_input["text"]
    options = ["-f", input_format, "-t", output_format]

    try:
        # Act
        result = call_pandoc(options=options, input_text=input_text)
    except PandocUnknownReaderError:
        if input_format in pandoc_input_formats:
            raise
        pass
    except PandocUnknownWriterError:
        if output_format in pandoc_output_formats:
            raise
        pass
    except PandocError:
        pytest.fail("PandocError raised during conversion.")
    else:
        # Assert
        assert isinstance(result, str)
        assert len(result) > 0


@settings(deadline=None)
@given(
    output_format=st.sampled_from(BINARY_OUTPUT_FORMATS),
    sample_input=st.sampled_from(EXAMPLE_DOCUMENTS),
)
def test_output_to_bytes(
    output_format, sample_input, pandoc_input_formats, pandoc_output_formats
):
    # Arrange
    input_format = sample_input["format"]
    input_text = sample_input["text"]
    options = ["-f", input_format, "-t", output_format, "-o", "-"]

    try:
        # Act
        result = call_pandoc(options=options, input_text=input_text, decode=False)
    except PandocUnknownReaderError:
        if input_format in pandoc_input_formats:
            raise
        pass
    except PandocUnknownWriterError:
        if output_format in pandoc_output_formats:
            raise
        pass
    except (PandocPDFProgramNotFoundError, PandocIOError):
        pytest.xfail("No PDF program found.")
    except PandocError:
        pytest.fail("PandocError raised during conversion.")
    else:
        # Assert
        assert isinstance(result, bytes)
        assert len(result) > 0


@settings(deadline=None)
@given(
    output_format=st.sampled_from(BINARY_OUTPUT_FORMATS),
    sample_input=st.sampled_from(EXAMPLE_DOCUMENTS),
)
def test_raises_unicode_error_when_decoding_binary_output(
    output_format, sample_input, pandoc_input_formats, pandoc_output_formats
):
    # Arrange
    input_format = sample_input["format"]
    input_text = sample_input["text"]
    options = ["-f", input_format, "-t", output_format, "-o", "-"]

    with pytest.raises(UnicodeError):
        try:
            # Act
            call_pandoc(options=options, input_text=input_text, decode=True)
        except PandocUnknownReaderError:
            if input_format in pandoc_input_formats:
                raise
            pass
        except PandocUnknownWriterError:
            if output_format in pandoc_output_formats:
                raise
            pass
        except (PandocPDFProgramNotFoundError, PandocIOError):
            pytest.xfail("No PDF program found.")
        except PandocError:
            pytest.fail("PandocError raised during conversion.")


def test_produces_output_with_url():
    options = ["-f", "html", "-t", "markdown"]

    try:
        result = call_pandoc(options=options, files=["https://example.com/"])
    except PandocHttpError:
        pytest.xfail("Connection failed.")
    else:
        assert isinstance(result, str)
        assert len(result) > 0


def test_cannot_provide_files_and_input_text():
    options = ["-f", "html", "-t", "markdown"]

    with pytest.raises(ValueError):
        call_pandoc(
            options=options, files=["https://example.com/"], input_text="# Example"
        )
