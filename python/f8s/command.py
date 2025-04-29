from pathlib import Path
import subprocess

import click
import lunchbox.theme as lbc
# ------------------------------------------------------------------------------

'''
Command line interface to f8s library
'''

click.Context.formatter_class = lbc.ThemeFormatter


@click.group()
def main():
    pass


@main.command()
def bash_completion():
    '''
    {white}BASH completion code to be written to a _f8s completion
    file.{clear}
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
    {white}Serves given F8s application via gunicorn.{clear}

    \b
    {cyan2}ARGUMENTS{clear}
        {cyan2}filepath{clear}  Filepath of F8s python module
             {cyan2}app{clear}  Name of app variable in module
    '''
    fp = Path(filepath)
    cmd = f'cd {fp.parent} && gunicorn --bind 0.0.0.0:8080 {fp.stem}:{app}'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()


@main.command()
def zsh_completion():
    '''
    {white}ZSH completion code to be written to a _f8s completion
    file.{clear}
    '''
    cmd = '_F8S_COMPLETE=zsh_source f8s'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result.wait()
    click.echo(result.stdout.read())


if __name__ == '__main__':
    main()
