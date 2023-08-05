import os
from datetime import date

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

  project_name = input("Type in the project name")

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


  pdf.add_page()
  pdf.cell(40,10, 'Animotions')
  pdf.cell(40,20, 'beyond the visual')

  files = [x for x in os.listdir(pov) if "CAM" in x]
  for f in files:
    pdf.add_page()
    camname = os.path.splitext(f)[0]
    pdf.cell(40,0, project_name)
    pdf.cell(40,10,camname)
    pdf.cell(40,20, proj_number)

  mv = os.path.join(cwd, 'MV')

  mvs = [int(x[0:1]) for x in os.listdir(mv)]

  print(max(mvs))

  datum = date.today().strftime("%Y%m%d")
  pdf.output(os.path.join(mv, f'{max(mvs)+1}_{datum}_pov_brief.pdf'), 'F')




  
