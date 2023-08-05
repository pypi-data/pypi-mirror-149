from typing import Optional


def get_exception_by_error_code(error_code: Optional[int]):
    """Get the pandoc exception corresponding to a given error code."""
    if error_code:
        try:
            specific_error = PANDOC_ERROR_CODES[error_code]
        except KeyError:
            raise ValueError(
                f"Error code {error_code} is not a known error code."
            ) from None
        else:
            specific_error.code = error_code
            return specific_error

    return PandocError


class PandocError(Exception):
    pass


class PandocIOError(PandocError):
    pass


class PandocFailOnWarningError(PandocError):
    pass


class PandocAppError(PandocError):
    pass


class PandocTemplateError(PandocError):
    pass


class PandocOptionError(PandocError):
    pass


class PandocUnknownReaderError(PandocError):
    pass


class PandocUnknownWriterError(PandocError):
    pass


class PandocUnsupportedExtensionError(PandocError):
    pass


class PandocCiteprocError(PandocError):
    pass


class PandocBibliographyError(PandocError):
    pass


class PandocEpubSubdirectoryError(PandocError):
    pass


class PandocPDFError(PandocError):
    pass


class PandocXMLError(PandocError):
    pass


class PandocPDFProgramNotFoundError(PandocError):
    pass


class PandocHttpError(PandocError):
    pass


class PandocShouldNeverHappenError(PandocError):
    pass


class PandocSomeError(PandocError):
    pass


class PandocParseError(PandocError):
    pass


class PandocParsecError(PandocError):
    pass


class PandocMakePDFError(PandocError):
    pass


class PandocSyntaxMapError(PandocError):
    pass


class PandocFilterError(PandocError):
    pass


class PandocLuaError(PandocError):
    pass


class PandocMacroLoop(PandocError):
    pass


class PandocUTF8DecodingError(PandocError):
    pass


class PandocIpynbDecodingError(PandocError):
    pass


class PandocUnsupportedCharsetError(PandocError):
    pass


class PandocCouldNotFindDataFileError(PandocError):
    pass


class PandocCouldNotFindMetadataFileError(PandocError):
    pass


class PandocResourceNotFound(PandocError):
    pass


PANDOC_ERROR_CODES = {
    1: PandocIOError,
    3: PandocFailOnWarningError,
    4: PandocAppError,
    5: PandocTemplateError,
    6: PandocOptionError,
    21: PandocUnknownReaderError,
    22: PandocUnknownWriterError,
    23: PandocUnsupportedExtensionError,
    24: PandocCiteprocError,
    25: PandocBibliographyError,
    31: PandocEpubSubdirectoryError,
    43: PandocPDFError,
    44: PandocXMLError,
    47: PandocPDFProgramNotFoundError,
    61: PandocHttpError,
    62: PandocShouldNeverHappenError,
    63: PandocSomeError,
    64: PandocParseError,
    65: PandocParsecError,
    66: PandocMakePDFError,
    67: PandocSyntaxMapError,
    83: PandocFilterError,
    84: PandocLuaError,
    91: PandocMacroLoop,
    92: PandocUTF8DecodingError,
    93: PandocIpynbDecodingError,
    94: PandocUnsupportedCharsetError,
    97: PandocCouldNotFindDataFileError,
    98: PandocCouldNotFindMetadataFileError,
    99: PandocResourceNotFound,
}
