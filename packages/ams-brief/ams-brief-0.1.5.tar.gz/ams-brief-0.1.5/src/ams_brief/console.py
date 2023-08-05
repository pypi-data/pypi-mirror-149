import os

import click

def main():
  cwd = os.getcwd()
  if cwd[0] != 'X':
    click.secho("Please run the tool in the X:/ drive")
    return

  if len(cwd) == 3:
    click.secho('Please run tool inside a project folder')
    return

  proj_number = cwd[3:7] 

  if len(proj_number) != 4:
    click.secho('probber')

  print(proj_number)

  stills = os.path.join(cwd, 'Test_Stills', 'POV')

  if not os.path.isdir(stills):
    click.secho(f"You need a folder called 'Test_Stills' inside {cwd}")
    return
  
  files = os.listdir(stills)
  for f in files:
    print(f)
  
