"""Dispatch argument to the different SMAP modules"""
import argparse
import logging
import sys
import colorlog
import matplotlib
import pkg_resources

from smap import __version__

matplotlib.use('Agg')


def main(args=None):
    """
    Parse all arguments to find which SMAP module to execute.
    Dispatch the rest of the argument to the chosen SMAP module for execution.
    Enable debug information if necessairy (tracelogs and show logger.debug calls).
    """
    if args is None:
        args = sys.argv[1:]
    modules = {entrypoint.name: entrypoint.load()
               for entrypoint in pkg_resources.iter_entry_points('modules')}
    main_arg_parser = argparse.ArgumentParser('SMAP', add_help=False)
    main_arg_parser.add_argument("module", choices=modules.keys())
    main_arg_parser.add_argument("--debug", help="Enable verbose logging.", action="store_true")
    parsed_args, remainder = main_arg_parser.parse_known_args(args)

    if parsed_args.debug:
        level = logging.DEBUG
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
    else:
        level = logging.INFO
        sys.tracebacklimit = 0  # Suppress traceback information on errors.

    handler = logging.StreamHandler(sys.stdout)
    formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s %(name)s - %(levelname)s: %(message)s',
                log_colors={
                    'DEBUG':    'reset',
                    'INFO':     'reset',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
                }
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level=level,
                        handlers=[handler])
    logging.info('This is SMAP %s', __version__)
    modules[parsed_args.module](remainder)


if __name__ == '__main__':
    main()
