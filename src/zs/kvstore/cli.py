
import json
import click
from zs.kvstore import KVStore, FOLDER_PATH
import os

@click.group()
def cli():
    pass

@cli.command()
@click.argument("key", type=str)
@click.option("-c", "--clipboard", is_flag=True)
def get(key, clipboard):
    if key not in KVStore.INDEX:
        click.echo(f"Key {key} not found")
        return
    if clipboard:
        from tkinter import Tk
        Tk().clipboard_set(KVStore.get(key))
        click.echo(f"Copied {key} to clipboard")
    else:
        click.echo(KVStore.get(key))

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
        json.dump(KVStore.INDEX, f)
    click.echo("KVStore exported")

@cli.command()
@click.argument("key", type=str)
@click.argument("file", type=click.Path())
@click.option("-a", "--append", is_flag=True)
def touch(key, file, append):
    mode = "a" if append else "w"
    with open(file, mode, encoding="utf-8") as f:
        f.write(KVStore.get(key))
    click.echo(f"KVStore touched {key} to {file}")

@cli.command()
def keys():
    for key in KVStore.INDEX.keys():
        click.echo(key)

@cli.command()
@click.argument("key", type=str)
def delete(key):
    KVStore.delete(key)
    click.echo(f"Deleted {key}")

@cli.command()
@click.option("-s", "--start", type=str, default="" , help="Starts with this string")
def list(start):
    for key in KVStore.INDEX.keys():
        if key.startswith(start):
            click.echo(key)

@cli.command()
@click.argument("key", type=str)
@click.option("-c", "--coder", is_flag=True)
@click.option("-s", "--simple", is_flag=True)
def edit(key, coder, simple):
    if key not in KVStore.INDEX:
        click.echo(f"Key {key} not found")
        return
    # get current contents
    content = KVStore.get(key)
    
    # dump to a file
    with open(os.path.join(FOLDER_PATH, key), "w", encoding="utf-8") as f:
        f.write(content)
    # open in notepad
    if coder:
        os.system(f"code {os.path.join(FOLDER_PATH, key)}")
        print(f"Opened {os.path.join(FOLDER_PATH, key)} in VS Code")
    elif simple:
        # if windows
        if os.name == "nt": 
            os.system(f"notepad {os.path.join(FOLDER_PATH, key)}")
            print(f"Opened {os.path.join(FOLDER_PATH, key)} in Notepad")
        # if linux
        elif os.name == "posix":
            os.system(f"gedit {os.path.join(FOLDER_PATH, key)}")
            print(f"Opened {os.path.join(FOLDER_PATH, key)} in Gedit")
        # if mac
        elif os.name == "mac":
            os.system(f"open {os.path.join(FOLDER_PATH, key)}")
            print(f"Opened {os.path.join(FOLDER_PATH, key)} in TextEdit")

        else:
            raise Exception("Unsupported OS")
        
    else:
        os.startfile(os.path.join(FOLDER_PATH, key))
        print(f"Opened {os.path.join(FOLDER_PATH, key)}")
        input("Press Enter to Save...")
    
    # save the file content back to index
    with open(os.path.join(FOLDER_PATH, key), "r", encoding="utf-8") as f:
        KVStore.set(key, f.read())
    click.echo(f"Saved {os.path.join(FOLDER_PATH, key)}")

if __name__ == "__main__":
    cli()

