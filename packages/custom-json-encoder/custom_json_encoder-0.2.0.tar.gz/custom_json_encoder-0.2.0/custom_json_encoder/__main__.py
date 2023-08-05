#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Javier Escalada Gómez
All rights reserved.
License: BSD 3-Clause Clear License (see LICENSE for details)
"""

# WARNING: This is a copy & paste & patch version from
# https://github.com/python/cpython/blob/3.10/Lib/json/tool.py
# For future versions follow the same algorithm.

from custom_json_encoder import CustomJSONEncoder

import argparse
import json
import sys
from pathlib import Path

#region patch
def config_indent_hint(options):
    def indent_hint(path, collection, indent, width):
        if options.indent is not None:
            return True
        if len(collection) == 0:
            return False
        if len(path) == 0:
            return True
        if path[-1] in options.indent_after:
            return True
        return False
    return indent_hint
#endregion

def main():
#region patch
    #prog = 'python -m json.tool'
    prog = 'custom_json_encoder'
#endregion
    description = ('A simple command line interface for json module '
                   'to validate and pretty-print JSON objects.')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType(encoding="utf-8"),
                        help='a JSON file to be validated or pretty-printed',
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?',
                        type=Path,
                        help='write the output of infile to outfile',
                        default=None)
    parser.add_argument('--sort-keys', action='store_true', default=False,
                        help='sort the output of dictionaries alphabetically by key')
    parser.add_argument('--no-ensure-ascii', dest='ensure_ascii', action='store_false',
                        help='disable escaping of non-ASCII characters')
    parser.add_argument('--json-lines', action='store_true', default=False,
                        help='parse input using the JSON Lines format. '
                        'Use with --no-indent or --compact to produce valid JSON Lines output.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--indent',
#region patch
                       default=None,
#endregion
                       type=int,
                       help='separate items with newlines and use this number '
                       'of spaces for indentation')
#region patch
    group.add_argument('--indent-after', action='append', default=[],
                       metavar='KEY',
                       help='indent after the given key using '
                       '--indent-after-indentation spaces')
#endregion
    group.add_argument('--tab', action='store_const', dest='indent',
                       const='\t', help='separate items with newlines and use '
                       'tabs for indentation')
#region patch
    # group.add_argument('--no-indent', action='store_const', dest='indent',
    #                    const=None,
    #                    help='separate items with spaces rather than newlines')
#endregion
    group.add_argument('--compact', action='store_true',
                       help='suppress all whitespace separation (most compact)')
#region patch
    parser.add_argument('--indent-after-width', default=80, type=int, metavar='AMOUNT',
                       help='set the width of the output line when '
                        '--indent-after is active')
    parser.add_argument('--indent-after-indentation', default=2, type=int,
                        metavar='AMOUNT',
                        help='use this number of spaces for indentation when '
                        '--indent-after is active')
#endregion
    options = parser.parse_args()

    dump_args = {
        'sort_keys': options.sort_keys,
        'indent': options.indent or options.indent_after_indentation,
        'ensure_ascii': options.ensure_ascii,
#region patch
        'cls': CustomJSONEncoder,
        'width': options.indent_after_width,
        'indent_hint': config_indent_hint(options),
#endregion
    }
    if options.compact:
        dump_args['indent'] = None
        dump_args['separators'] = ',', ':'

    with options.infile as infile:
        try:
            if options.json_lines:
                objs = (json.loads(line) for line in infile)
            else:
                objs = (json.load(infile),)

            if options.outfile is None:
                out = sys.stdout
            else:
                out = options.outfile.open('w', encoding='utf-8')
            with out as outfile:
                for obj in objs:
                    json.dump(obj, outfile, **dump_args)
                    outfile.write('\n')
        except ValueError as e:
            raise SystemExit(e)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError as exc:
        sys.exit(exc.errno)
