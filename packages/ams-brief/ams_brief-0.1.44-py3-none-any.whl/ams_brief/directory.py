from pathlib import Path
from pick import pick
import click
import os

filters = [
    "Mails&Vergaderingen",
    "ScriptGenerated",
    "MV",
    "Maps",
    "Proxy",
    "Xref",
    "Autoback",
    "AutoBackup",
    "Output",
    "Script",
    "renderpresets",
    "OnlineTool_Lab",
    "Documentatie"
]


def get_images(rootdir):
    os.system('cls' if os.name == 'nt' else 'clear')

    options = []
    for path in Path(rootdir).rglob('**'):
        if path.is_dir() and not any([x in str(path) for x in filters]):
            files = [x for x in path.iterdir() if x.suffix == '.jpg']
            if len(files) > 0:
                options.append(path)
                # for f in files:
                #   print(f)
    option = pick(options, f"👋 {os.getlogin()}, pick a folder:", '=>')

    click.secho(f"🥳 You have selected {option[0]}!", fg='green')
    print(f"💁‍♀️ Here are the renders we found in {option[0]}:\n")

    for f in [x for x in Path(option[0]).iterdir() if x.is_file() and x.suffix == '.jpg']:
        print(f.name)

    while True:
        response = input(
            "\n🕵️‍♂️ Type 'y' or 'yes' to continue, 'n' or 'No' to start over...")
        if response == 'y' or response == 'Y' or response == 'yes':
            click.secho(f"👊 Ok, we're going with {option[0]}", fg='green')
            return option[0]
        elif response == 'n' or response == 'N' or response == 'no':
            click.secho("🙅‍♂️ Ok, we outta dis", fg='red')
            quit()
        else:
            print('no understandooooo')
            continue
