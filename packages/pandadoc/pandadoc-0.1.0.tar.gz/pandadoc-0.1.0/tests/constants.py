BINARY_OUTPUT_FORMATS = [
    "docx",
    "epub",
    "epub2",
    "epub3",
    "odt",
    "pdf",
    "pptx",
]
TEXT_OUTPUT_FORMATS = [
    "asciidoc",
    "asciidoctor",
    "beamer",
    "commonmark",
    "commonmark_x",
    "context",
    "csljson",
    "docbook",
    "docbook4",
    "docbook5",
    "dokuwiki",
    "dzslides",
    "fb2",
    "gfm",
    "haddock",
    "html",
    "html4",
    "html5",
    "icml",
    "ipynb",
    "jats",
    "jats_archiving",
    "jats_articleauthoring",
    "jats_publishing",
    "jira",
    "json",
    "latex",
    "man",
    "markdown",
    "markdown_github",
    "markdown_mmd",
    "markdown_phpextra",
    "markdown_strict",
    "markua",
    "mediawiki",
    "ms",
    "muse",
    "native",
    "opendocument",
    "opml",
    "org",
    "plain",
    "revealjs",
    "rst",
    "rtf",
    "s5",
    "slideous",
    "slidy",
    "tei",
    "texinfo",
    "textile",
    "xwiki",
    "zimwiki",
]
BIB_OUTPUT_FORMATS = [
    "biblatex",
    "bibtex",
]

# Tuple of example documents and their types
EXAMPLE_DOCUMENTS = [
    {
        "format": "markdown",
        "text": """% Example Document
% Chris
% Feb 23rd, 2022

# Simple example

A simple example of a pandoc markdown document for testing purposes.

    Including indented text

And *italic*, **bold**, `mono` text

And a URL to <https://example.com/>.""",
    },
]

# Tuple of example URLs and their types
EXAMPLE_URLS = [
    ("html", "https://example.com/"),
    ("markdown", "https://pandoc.org/demo/MANUAL.txt"),
    ("latex", "https://pandoc.org/demo/example4.tex"),
]
