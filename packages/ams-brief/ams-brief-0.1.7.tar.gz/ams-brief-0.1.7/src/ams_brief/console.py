import os

import click

from fpdf import FPDF 


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

  stills = os.path.join(cwd, 'Test_Stills')

  if not os.path.isdir(stills):
    click.secho(f"You need a folder called 'Test_Stills' inside {cwd}")
    return

  pov = os.path.join(stills, 'POV')

  if not os.path.isdir(pov):
    click.secho(f"You need a folder called 'POV' inside {stills}")
    return

  pdf = FPDF(orientation='L', format='A4')
  pdf.set_font('Arial', 'B', 16)


  files = os.listdir(pov)
  for f in files:
    pdf.add_page()
    pdf.cell(40,10,f)
    pdf.cell(40,20, proj_number)

  mv = os.path.join(cwd, 'MV')

  pdf.output(mv, 'pov_brief.pdf', 'F')




  
