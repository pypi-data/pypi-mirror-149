import os

import click

def main():
  cwd = os.getcwd()
  if cwd[0] != 'X':
    click.secho("Please run the briefing tool in the X:/ drive")
    return
  

  print('hey')
