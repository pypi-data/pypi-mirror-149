.. image:: https://raw.githubusercontent.com/chris-mcdo/pandadoc/main/panda.svg
   :align: center
   :height: 200
   :alt: pandadoc


pandadoc: lightweight pandoc wrapper
====================================

.. image:: https://img.shields.io/pypi/v/pandadoc.svg
  :target: https://pypi.org/project/pandadoc/
  :alt: Project Version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/pandadoc.svg
  :target: https://pypi.org/project/pandadoc/
  :alt: Supported Python Versions

.. image:: https://github.com/chris-mcdo/pandadoc/workflows/tests/badge.svg
  :target: https://github.com/chris-mcdo/pandadoc/actions?query=workflow%3Atests
  :alt: Unit Tests

.. image:: https://codecov.io/gh/chris-mcdo/pandadoc/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/chris-mcdo/pandadoc
  :alt: Unit Test Coverage

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black
  :alt: Code Style: Black

.. image:: https://img.shields.io/badge/license-MIT-purple
  :target: https://github.com/chris-mcdo/pandadoc/blob/main/LICENSE
  :alt: MIT License


An extremely lightweight `pandoc <https://pandoc.org/>`_ wrapper for Python 3.8+.

Its features:

- Supports conversion between all formats that ``pandoc`` supports -
  markdown, HTML, LaTeX, Word, epub, pdf (output),
  `and more <https://pandoc.org/demos.html>`_.

- Output to raw ``bytes`` (binary formats - e.g. PDF), to ``str`` objects
  (text formats - e.g. markdown), or to file (any format).

- ``pandoc`` errors are raised as (informative) exceptions.

- Full flexibility of the ``pandoc`` command-line tool, and the same syntax. (See the
  `pandoc manual <https://pandoc.org/MANUAL.html>`_ for more information.)

Getting Started Guide
*********************

Installation
------------

First, ensure ``pandoc`` is on your ``PATH``.
(In other words, `install pandoc <https://pandoc.org/installing.html>`_ and add it to
your ``PATH``.)

Then install ``pandadoc`` from `PyPI <https://pypi.org/project/pandadoc/>`_:

.. code-block:: console

    $ python -m pip install pandadoc

That's it.

Usage
-----

Convert a webpage to markdown, and store it as a python ``str``:

.. code-block:: python

    >>> import pandadoc
    >>> input_url = "https://example.com/"
    >>> example_md = pandadoc.call_pandoc(
    ...    options=["-t", "markdown"], files=[input_url]
    ... )
    >>> print(example_md)
    <div>

    # Example Domain
    
    This domain is for use in illustrative examples in documents.
    ...

Now convert the markdown to RTF, and write it to a file:

.. code-block:: python

    >>> rtf_output_file = "example.rtf"
    >>> pandadoc.call_pandoc(
    ...     options=["-f", "markdown", "-t", "rtf", "-o", rtf_output_file], 
    ...     input_text=example_md,
    ... )
    ''

Notice that ``call_pandoc`` returns an empty string ``''`` when a file output is used.
Looking at the output file:

::

    {\pard \ql \f0 \sa180 \li0 \fi0 \outlinelevel0 \b \fs36 Example Domain\par}
    {\pard \ql \f0 \sa180 \li0 \fi0 This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\par}
    {\pard \ql \f0 \sa180 \li0 \fi0 {\field{\*\fldinst{HYPERLINK "https://www.iana.org/domains/example"}}{\fldrslt{\ul
    More information...
    }}}
    \par}

Convert this RTF document to PDF, using xelatex with a custom character set,
and store the result as raw ``bytes``:

.. code-block:: python

    >>> raw_pdf = pandadoc.call_pandoc(
    ...     options=["-f", "markdown", "-t", "pdf", "--pdf-engine", "xelatex", "--variable-mainfont",  "Palatino"],
    ...     files=[rtf_output_file],
    ...     decode=False,
    ... )

Note that PDF conversion requires a
"`PDF engine <https://pandoc.org/MANUAL.html#creating-a-pdf>`_"
(e.g. pdflatex, latexmk etc.) to be installed.

Now you can send those raw bytes over a network, or write them to a file:

.. code-block:: python

    >>> with open("example.pdf", "wb") as f:
    ...     f.write(raw_pdf)
    ... 
    >>> # Finished

You can find more ``pandoc`` examples `here <https://pandoc.org/demos.html>`_.

Exceptions
----------

If ``pandoc`` exits with an error, an appropriate exception is raised (based on the
`exit code <https://pandoc.org/MANUAL.html#exit-codes>`_):

.. code-block:: python

    >>> pandadoc.call_pandoc(
    ...     options=["-f", "markdown", "-t", "zzz"], # non-existent format
    ...     input_text=example_md,
    ... )
    Traceback (most recent call last):
    ...
    pandadoc.exceptions.PandocUnknownWriterError: Unknown output format zzz
    >>> isinstance(pandadoc.exceptions.PandocUnknownWriterError(), pandadoc.PandocError)
    True

You can find a full list of exceptions in the ``pandadoc.exceptions`` module.

Explanation
-----------

The ``pandoc`` command-line tool works like this::

    pandoc [OPTIONS] [FILES]

In addition to the ``OPTIONS``
(`documented here <https://pandoc.org/MANUAL.html#options>`_),
you can provide either some ``FILES``, or some input text (via ``stdin``).

The ``call_pandoc`` function of ``pandadoc`` works in a similar way:

- The ``options`` argument contains a list of pandoc options.
  E.g. ``["-f", "markdown", "-t", "html"]``.

- The ``files`` argument is a list of file paths (or absolute URIs).
  E.g. ``["path/to/file.md", "https://www.fsf.org"]``

- The ``input_text`` argument is used as text input to pandoc.
  E.g. ``# Simple Doc\n\nA simple markdown document\n``.

The ``timeout`` and ``decode`` arguments are used to control whether the ``pandoc``
process times out, and whether the result should be decoded to a ``str``
(``True`` by default).

Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/chris-mcdo/pandadoc/issues>`_
to submit bugs or request features.

Feedback is always appreciated.

License
-------

Distributed under the
`MIT license <https://github.com/chris-mcdo/pandadoc/blob/main/LICENSE>`_.
