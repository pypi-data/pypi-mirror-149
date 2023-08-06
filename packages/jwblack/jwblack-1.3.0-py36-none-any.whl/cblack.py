#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

import black
from black.strings import normalize_string_prefix, get_string_prefix
from black.nodes import is_docstring, is_multiline_string

__version__ = '1.3.0'

_orgLineStr = black.Line.__str__
_orgFixDocString = black.linegen.fix_docstring


def lineStrIndentTwoSpaces(self) -> str:
  """Intended to replace Line.__str__ to produce 2-space indentation blocks
  instead of the 4 by default.
  """

  original = _orgLineStr(self)
  if not original.startswith(' '):
    return original

  noLeftSpaces = original.lstrip(' ')
  nLeadingSpaces = len(original) - len(noLeftSpaces)

  # reindent by generating half the spaces (from 4-space blocks to 2-space blocks)
  reindented = '%s%s' % (' ' * (nLeadingSpaces >> 1), noLeftSpaces)
  return reindented


def fixDocString(docstring, prefix):
  """Indent doc strings by 2 spaces instead of 4"""
  return _orgFixDocString(docstring, ' ' * (len(prefix) >> 1))


def fix_doc(self, leaf):
  if is_docstring(leaf) and "\\\n" not in leaf.value:
    # We're ignoring docstrings with backslash newline escapes because changing
    # indentation of those changes the AST representation of the code.
    docstring = normalize_string_prefix(leaf.value)
    prefix = get_string_prefix(docstring)
    docstring = docstring[len(prefix):]  # Remove the prefix
    quote_char = docstring[0]
    # A natural way to remove the outer quotes is to do:
    #   docstring = docstring.strip(quote_char)
    # but that breaks on """""x""" (which is '""x').
    # So we actually need to remove the first character and the next two
    # characters but only if they are the same as the first.
    quote_len = 1 if docstring[1] != quote_char else 3
    docstring = docstring[quote_len:-quote_len]
    docstring_started_empty = not docstring

    if is_multiline_string(leaf):
      indent = " " * 4 * self.current_line.depth
      docstring = fixDocString(docstring, indent)
    else:
      docstring = docstring.strip()

    if docstring:
      # Add some padding if the docstring starts / ends with a quote mark.
      if docstring[0] == quote_char:
        docstring = " " + docstring
      if docstring[-1] == quote_char:
        docstring += " "
      if docstring[-1] == "\\":
        backslash_count = len(docstring) - len(docstring.rstrip("\\"))
        if backslash_count % 2:
          # Odd number of tailing backslashes, add some padding to
          # avoid escaping the closing string quote.
          docstring += " "
    elif not docstring_started_empty:
      docstring = " "

    # We could enforce triple quotes at this point.
    quote = quote_char * quote_len
    leaf.value = prefix + quote + docstring + quote

  yield from self.visit_default(leaf)


black.Line.__str__ = lineStrIndentTwoSpaces
black.LineGenerator.visit_STRING = fix_doc


def main():
  # behabe like normal black code
  sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
  sys.exit(black.main())


if __name__ == '__main__':
  sys.exit(main())
