import os

import click

def main():
  cwd = os.getcwd()
  if cwd[0] != 'X':
    click.secho("Please run the briefing tool in the X:/ drive")
    return
  
  proj_number = cwd[3:6] 
  print(proj_number)
  
  

  print('hey')
