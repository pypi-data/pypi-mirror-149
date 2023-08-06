#coding: utf8
from __future__ import absolute_import
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = (str, bytes)
    unicode = str
else:
    string_types = basestring
    unicode = unicode


def to_bytes(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return s

ENCODINGS = [
    "utf8",
    "gb18030",
    "big5",
    "latin1",
    "ascii"
]
def to_unicode(s):
    if not isinstance(s, unicode):
        try:
            s = unicode(s)
            return s
        except:
            pass
        for encoding in ENCODINGS:
            try:
                s = unicode(s, encoding)
                return s
            except:
                pass
    return s

smart_unicode = to_unicode
smart_str = to_bytes


class UnicodeWithAttrs(unicode):
    pass
