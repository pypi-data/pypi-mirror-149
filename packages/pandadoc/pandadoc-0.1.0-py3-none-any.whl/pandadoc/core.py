import subprocess
from typing import Literal, Optional, Sequence, Union, overload

from pandadoc.exceptions import get_exception_by_error_code


@overload
def call_pandoc(
    options: Sequence[str],
    files: Optional[Sequence[str]] = None,
    input_text: Optional[str] = None,
    timeout: Optional[float] = None,
    decode: Literal[True] = ...,
) -> str:
    ...  # pragma: no cover


@overload
def call_pandoc(
    options: Sequence[str],
    files: Optional[Sequence[str]] = None,
    input_text: Optional[str] = None,
    timeout: Optional[float] = None,
    *,
    decode: Literal[False],
) -> bytes:
    ...  # pragma: no cover


def call_pandoc(
    options: Sequence[str],
    files: Optional[Sequence[str]] = None,
    input_text: Optional[str] = None,
    timeout: Optional[float] = None,
    decode: bool = True,
) -> Union[str, bytes]:
    """Call pandoc and return any output.

    At most one of `text` and `files` can be provided.

    For more information on pandoc options, see https://pandoc.org/MANUAL.html.

    Parameters
    ----------
    options
        A list of pandoc options. E.g. ``["-f", "markdown", "-t", "html"]``.
    files
        A list of paths (or absolute URIs) to input data. E.g. ``["path/to/file.md",
        "https://www.fsf.org"]``.
    input_text
        Text input to pandoc. E.g. ``# Simple Doc\n\nA simple markdown document\n``.
    timeout
        A timeout for the called process.
    decode
        Whether to decode the result to a ``str``, or leave the result as UTF-8-encoded
        ``bytes``.

    Returns
    -------
    The result returned by pandoc, either as a string (if ``decode=True``) or
    UTF-8-encoded bytes (if ``decode=False``). Empty if an output file is specified.

    Raises
    ------
    TimeoutExpired
        If the process takes longer than `timeout` to complete.
    PandocError
        ``PandocError`` or a subclass of ``PandocError`` is raised if the process
        exits with a non-zero exit code.
    UnicodeError
        If `decode` is True and the result could not be decoded.
    """
    # Clean arguments
    if input_text and files:
        raise ValueError("Both input_text and files were provided.")

    if files is None:
        files = []

    input = None
    if input_text is not None:
        input: bytes = input_text.encode(encoding="utf-8")

    args: Sequence[str] = ["pandoc", *options, *files]

    # Run pandoc
    pandoc_process = subprocess.run(
        args, input=input, capture_output=True, timeout=timeout
    )

    # Raise exception if needed
    if (error_code := pandoc_process.returncode) > 0:
        message = pandoc_process.stderr.decode("utf-8")
        raise get_exception_by_error_code(error_code)(message)

    # Return
    if decode:
        try:
            return pandoc_process.stdout.decode(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise UnicodeError(
                "Could not decode pandoc output."
                " (Maybe you meant to set `decode` to False?)"
            ) from exc
    else:
        return pandoc_process.stdout
