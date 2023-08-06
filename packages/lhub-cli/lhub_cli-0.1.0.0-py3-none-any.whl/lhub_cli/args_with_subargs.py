#!/usr/bin/env python
import argparse

# # create the top-level parser
# parser = argparse.ArgumentParser(prog='PROG')
# parser.add_argument('--foo', action='store_true', help='foo help')
# subparsers = parser.add_subparsers(help='sub-command help')
#
# # create the parser for the "a" command
# parser_a = subparsers.add_parser('a', help='a help')
# parser_a.add_argument('bar', type=int, help='bar help')
#
# # create the parser for the "b" command
# parser_b = subparsers.add_parser('b', help='b help')
# parser_b.add_argument('--baz', choices='XYZ', help='baz help')
#
# # parse some argument lists
# parser.parse_args(['a', '12'])
#
# parser.parse_args(['--foo', 'b', '--baz', 'Z'])
#
# _args = parser.parse_args()

# create the top-level parser
parser = argparse.ArgumentParser(prog='lhub')

# parser.add_argument("x", type=str, help="Some text")

parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_command = subparsers.add_parser('command', help='command help')
parser_command.add_argument('command', metavar='COMMAND_NAME', type=str, help='command name')

# create the parser for the "b" command
parser_playbook = subparsers.add_parser('playbook', help='playbook help')
parser_playbook.add_argument('playbook', metavar='PLAYBOOK_NAME', type=str, help='playbook name')
# parser_playbook.add_argument('--option', choices='XYZ', help='option help')

# parse some argument lists
# parser.parse_args(['command', '12'])

# parser.parse_args(['--foo', 'b', '--baz', 'Z'])

_args = parser.parse_args()

print(dir(_args))
