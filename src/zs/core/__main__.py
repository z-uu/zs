import os
import sys
import click
import zs.core
import subprocess

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
    if exe in zs.core.INSTALLED:
        click.echo(f"Already installed: {exe}")
        return
    if exe not in zs.core.INDEX:
        click.echo(f"Not found: {exe}")
        return
    
    git_url = zs.core.INDEX[exe]["git_url"].split("://")[1]
    git_url = "https://" + git_url  
    os.system(f"{sys.executable} -m pip install git+{git_url}")

@cli.command()
@click.argument("exe", type=str)
def uninstall(exe):
    if exe not in zs.core.INSTALLED:
        click.echo(f"Not installed: {exe}")
        return
    os.system(f"{sys.executable} -m pip uninstall {exe}")

@cli.command()
@click.argument("exe", type=str, required=False)
@click.option("--all", is_flag=True)
def update(exe, all):
    if not all and not exe:
        click.echo("Please provide either an executable name or --all flag")
        return
    
    if all:
        # update zs first
        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "zs"])

        for exe in zs.core.INSTALLED:
            if exe == "zs":
                continue
            subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", exe])
        return
    
    if exe not in zs.core.INSTALLED:
        click.echo(f"Not installed: {exe}")
        return
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", exe])

if __name__ == "__main__":
    cli()
