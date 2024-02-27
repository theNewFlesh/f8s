import subprocess
import sys

import click
from gunicorn.app.wsgiapp import run
# ------------------------------------------------------------------------------

'''
Command line interface to f8s library
'''


@click.group()
def main():
    pass


@main.command()
def bash_completion():
    '''
    BASH completion code to be written to a _f8s completion file.
    '''
    cmd = '_F8S_COMPLETE=bash_source f8s'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


@main.command()
@click.argument('module', type=str, nargs=1)
@click.argument('app', type=str, nargs=1, default='app')
def serve(module, app):
    # type: (str, str) -> None
    '''
    Serves given F8s application.

    \b
    Arguments:
        MODULE - Module name of Flask app
        APP - Name of app variable
    '''
    sys.argv = ['-c', '--bind', '0.0.0.0:8080', f'{module}:{app}']
    run()


@main.command()
def zsh_completion():
    '''
    ZSH completion code to be written to a _f8s completion file.
    '''
    cmd = '_F8S_COMPLETE=zsh_source f8s'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


if __name__ == '__main__':
    main()
