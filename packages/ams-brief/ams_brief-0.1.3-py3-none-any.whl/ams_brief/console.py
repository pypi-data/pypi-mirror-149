import os

import click

def main():
  cwd = os.getcwd()
  if cwd[0] != 'X':
    click.secho("Please run the briefing tool in the X:/ drive")
    return
  print(len(cwd)) 
  proj_number = cwd[3:7] 
  
  print(proj_number)
  
  

  print('hey')
