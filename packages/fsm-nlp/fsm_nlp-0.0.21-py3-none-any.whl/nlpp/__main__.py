"""
nlpp - Content Analysis Toolkit for python
CLI module
"""
import sys
import logging

# logging block
logging.basicConfig(filename='/home/philippy/py/base-nlpp/nlpp.log', level=logging.DEBUG, format='%(asctime)s | %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARNING)
log.addHandler(handler)

HELP_TEXT = """nlpp installation setup

Run

    python -m nlpp setup

to install."""

if __name__ == '__main__':
    import subprocess
    import json

    log.debug('debug')
    log.info('info')
    log.warning("Error message stdout")

    # try:
    #     from tmtoolkit.corpus import DEFAULT_LANGUAGE_MODELS
    # except ImportError:
    #     print('error: tmtoolkit is not installed with the dependencies required for text processing; '
    #           'install tmtoolkit with the [recommended] or [textproc] option', file=sys.stderr)
    #     exit(1)

    def _setup(args):
        # from spacy.cli.download import download
        pass


    def _help(args):
        print(HELP_TEXT)
        pass

    # commands = {
    #     'setup': _setup,
    #     'help': _help,
    # }

    # if len(sys.argv) <= 1:
    #     print('available commands: ' + ', '.join(commands.keys()))
    #     print('run `python -m tmtoolkit help` for help')
    #     exit(6)

    # cmd = sys.argv[1]
    # if cmd in commands.keys():
    #     commands[cmd](sys.argv[2:])
    # else:
    #     print('command not supported:', cmd, file=sys.stderr)
    #     exit(7)
