# coding: utf8
from __future__ import absolute_import
import re

from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, \
    default, using, words, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Punctuation, Number

from pygments.lexers.jvm import ScalaLexer
from pygments.lexers.css import CssLexer, _indentation, _starts_block



class JadeLexer(ExtendedRegexLexer):
    """
    For Jade markup.
    Jade is a variant of Scaml, see:
    http://scalate.fusesource.org/documentation/scaml-reference.html

    .. versionadded:: 1.4
    """

    name = 'Jade'
    aliases = ['jade']
    filenames = ['*.jade']
    mimetypes = ['text/x-jade']

    flags = re.IGNORECASE
    _dot = r'.'

    tokens = {
        'root': [
            (r'[ \t]*\n', Text),

            (r'//.*?\n', Comment), # comment

            (r'[ \t]*', _indentation),
        ],

        'css': [
            (r'(\s*)(\+|if +|elif +|else if +|[a-z0-9-_]+ += +)([a-z0-9-_]+)([a-z0-9-_\.]+)(\s*[=><\!].*)?(\n)', bygroups(Text, Operator, Keyword, Name.Attribute, Text, Text)),
            (r'(\s*)(\+|if +|elif +|else if +|[a-z0-9-_]+ += +)([a-z0-9-_]+)(?=[\. \t\(\[])([^\(\)]+)?(\(.*?\))?(\n)', bygroups(Text, Operator, Keyword, Name.Function, Punctuation, Text)),
            (r'\.[\w:-]+', Name.Class, 'tag'),
            (r'\#[\w:-]+', Name.Function, 'tag'),
        ],

        'eval-or-plain': [
            (r'[&!]?==', Punctuation, 'plain'),
            (r'([&!]?[=~])(' + _dot + r'*\n)',
             bygroups(Punctuation, using(ScalaLexer)),  'root'),
            default('plain'),
        ],

        'content': [
            include('css'),
            (r'!!!' + _dot + r'*\n', Name.Namespace, '#pop'),
            (r'(/)(\[' + _dot + '*?\])(' + _dot + r'*\n)',
             bygroups(Comment, Comment.Special, Comment),
             '#pop'),
            (r'/' + _dot + r'*\n', _starts_block(Comment, 'html-comment-block'),
             '#pop'),
            (r'-#' + _dot + r'*\n', _starts_block(Comment.Preproc,
                                                  'scaml-comment-block'), '#pop'),
            (r'(-@\s*)(import)?(' + _dot + r'*\n)',
             bygroups(Punctuation, Keyword, using(ScalaLexer)),
             '#pop'),
            (r'(-)(' + _dot + r'*\n)',
             bygroups(Punctuation, using(ScalaLexer)),
             '#pop'),
            (r':' + _dot + r'*\n', _starts_block(Name.Decorator, 'filter-block'),
             '#pop'),

            (r'\s*[\w:-]+', Name.Tag, 'tag'),

            (r'\|', Text, 'eval-or-plain'),
        ],

        'tag': [
            include('css'),
            (r'\{(,\n|' + _dot + ')*?\}', using(ScalaLexer)),
            (r'\[' + _dot + '*?\]', using(ScalaLexer)),
            (r'\(', Text, 'html-attributes'),
            (r'/[ \t]*\n', Punctuation, '#pop:2'),
            (r'[<>]{1,2}(?=[ \t=])', Punctuation),
            include('eval-or-plain'),
        ],

        'plain': [
            (r'([^#\n]|#[^{\n]|(\\\\)*\\#\{)+', Text),
            (r'(#\{)(' + _dot + '*?)(\})',
             bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
            (r'\n', Text, 'root'),
        ],

        'html-attributes': [
            (r'\s+', Text),
            (r'[\w:-]+[ \t]*=', Name.Attribute, 'html-attribute-value'),
            (r'[\w:-]+', Name.Attribute),
            (r'\)', Text, '#pop'),
        ],

        'html-attribute-value': [
            (r'[ \t]+', Text),
            (r'\w+', Name.Variable, '#pop'),
            (r'@\w+', Name.Variable.Instance, '#pop'),
            (r'\$\w+', Name.Variable.Global, '#pop'),
            (r"'(\\\\|\\'|[^'\n])*'", String, '#pop'),
            (r'"(\\\\|\\"|[^"\n])*"', String, '#pop'),
        ],

        'html-comment-block': [
            (_dot + '+', Comment),
            (r'\n', Text, 'root'),
        ],

        'scaml-comment-block': [
            (_dot + '+', Comment.Preproc),
            (r'\n', Text, 'root'),
        ],

        'filter-block': [
            (r'([^#\n]|#[^{\n]|(\\\\)*\\#\{)+', Name.Decorator),
            (r'(#\{)(' + _dot + '*?)(\})',
             bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
            (r'\n', Text, 'root'),
        ],
    }
