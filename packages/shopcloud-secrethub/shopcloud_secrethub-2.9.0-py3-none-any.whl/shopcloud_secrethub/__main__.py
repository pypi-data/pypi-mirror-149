import argparse
from . import cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SecretHub',
        prog='shopcloud-secrethub'
    )

    subparsers = parser.add_subparsers(help='commands', title='commands')

    parser_auth = subparsers.add_parser('auth', help='generate auth file')
    parser_auth.set_defaults(which='auth')

    parser_auth = subparsers.add_parser('token-refresh', help='generate new token')
    parser_auth.set_defaults(which='token-refresh')

    parser_read = subparsers.add_parser('read', help='read a secret')
    parser_read.add_argument('name', type=str, help='secret name')
    parser_read.add_argument('--output', '-o', help='Output Format', choices=['text', 'json', 'raw'])
    parser_read.set_defaults(which='read')

    parser_write = subparsers.add_parser('write', help='write a secret')
    parser_write.add_argument('name', type=str, help='secret name')
    parser_write.add_argument('value', type=str, help='secret value', nargs='?')
    parser_write.add_argument('--in-file', '-i', nargs='?', help='Use the contents of this file as the value of the secret.')
    parser_write.set_defaults(which='write')

    parser_inject = subparsers.add_parser('inject', help='inject the secrets')
    parser_inject.add_argument('-i', required=True)
    parser_inject.add_argument('-o', required=True)
    parser_inject.set_defaults(which='inject')

    parser_printenv = subparsers.add_parser('printenv', help='print as env export')
    parser_printenv.add_argument('-i', required=True)
    parser_printenv.set_defaults(which='printenv')

    args = parser.parse_args()
    cli.main(args)
