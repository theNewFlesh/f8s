from pathlib import Path
import subprocess

import click
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
@click.argument('filepath', type=str, nargs=1)
@click.argument('app', type=str, nargs=1, default='app')
def serve(filepath, app):
    # type: (str, str) -> None
    '''
    Serves given F8s application.

    \b
    Arguments:
        FILEPATH - Filepath of F8s python module
        APP - Name of app variable in module
    '''
    fp = Path(filepath)
    cmd = f'cd {fp.parent} && gunicorn --bind 0.0.0.0:8080 {fp.stem}:{app}'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()


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
