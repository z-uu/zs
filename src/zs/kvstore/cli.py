
import json
import click
from zs.kvstore import KVStore

@click.group()
def cli():
    pass

@cli.command()
@click.argument("key", type=str)
def get(key):
    if key not in KVStore.STORE:
        click.echo(f"Key {key} not found")
        return
    click.echo(KVStore.STORE[key])

@cli.command()
@click.argument("key", type=str)
@click.argument("value", type=str, required=False)
def set(key, value):
    if value is None:
        from tkinter import Tk
        value = Tk().clipboard_get()
    KVStore.set(key, value)
    click.echo(f"Set {key} to {value}")
@cli.command()
def reset():
    KVStore.clear()
    click.echo("KVStore reset")

@cli.command()
@click.argument("file", type=click.Path())
def export(file):
    with open(file, "w") as f:
        json.dump(KVStore, f)
    click.echo("KVStore exported")


@cli.command()
def keys():
    for key in KVStore.keys():
        click.echo(key)

@cli.command()
@click.argument("key", type=str)
def delete(key):
    KVStore.delete(key)
    click.echo(f"Deleted {key}")

if __name__ == "__main__":
    cli()

