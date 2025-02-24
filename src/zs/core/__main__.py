
import os
import sys
import click
import zs.core

@click.group()
def cli():
    pass

@cli.command()
def list():
    click.echo("=======builtin=======")
    click.echo("kvstore")
    click.echo("=======installed=======")
    for exe in zs.core.INSTALLED:
        click.echo(exe)

@cli.command()
@click.argument("exe", type=str)
def install(exe):
    os.system(f"{sys.executable} -m pip install ")

if __name__ == "__main__":
    cli()
