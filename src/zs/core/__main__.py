import os
import sys
import click
import zs.core
import subprocess

def get_git_url(exe):
    if exe not in zs.core.INDEX:
        return None
    git_url = zs.core.INDEX[exe]["git_url"].split("://")[1]
    return "https://" + git_url

@click.group()
def cli():
    pass

@cli.command()
def list():
    click.echo(sys.executable)
    click.echo("=======builtin=======")
    click.echo("kvstore")
    click.echo("=======installed=======")
    for exe in zs.core.get_installed():
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
    
    git_url = get_git_url(exe)
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
    
    if exe == "zs":
        click.echo("Updating self is not allowed, please run the following command instead:")
        click.echo("python -m pip install --upgrade git+https://github.com/z-uu/zs.git")
        return

    if all:
        for exe in zs.core.INSTALLED:
            if exe == "zs":
                continue
            git_url = get_git_url(exe)
            if git_url:
                subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", f"git+{git_url}"])
        return
    
    if exe not in zs.core.INSTALLED:
        click.echo(f"Not installed: {exe}")
        return
    git_url = get_git_url(exe)
    if not git_url:
        click.echo(f"Not found in index: {exe}")
        return
        
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", f"git+{git_url}"])

@cli.command()
def index():
    for exe in zs.core.INDEX:
        if exe == "zs":
            continue
        if exe in zs.core.INSTALLED:
            click.echo(f"{exe} (installed)")
        else:
            click.echo(f"{exe}")

if __name__ == "__main__":
    cli()
