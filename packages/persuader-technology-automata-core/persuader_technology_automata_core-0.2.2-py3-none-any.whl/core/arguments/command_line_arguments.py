import argparse

from core.arguments.ParseDictionaryArgs import ParseDictionaryArgs
from core.meta.MetaInfo import MetaInfo


def option_arg_parser() -> argparse.ArgumentParser:

    meta_info = MetaInfo()
    version = meta_info.get_version()
    description = meta_info.get_description()

    command_line_argument_parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description=description
    )

    command_line_argument_parser.add_argument(
        '-v', '--version', action='version',
        version=f'{command_line_argument_parser.prog} version {version}'
    )

    command_line_argument_parser.add_argument('--options', nargs='*', required=False, help=f'Specific options for {description}.', action=ParseDictionaryArgs)

    return command_line_argument_parser
