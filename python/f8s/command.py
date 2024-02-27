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
def serve():
    '''
        Serve Flask application.
    '''
    sys.argv = ['-c', '--bind', '0.0.0.0:8080', 'test_app:app']
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
