import os
from datetime import date

import click

from fpdf import FPDF 


def main():

  pdf = FPDF(orientation='L', format='A4')
  pdf.add_font(family='montserrat', fname=r"X:\9999_BID_AMS\AMS-VFB_Fonts\Montserrat-ExtraBold.ttf", uni=True)
  pdf.add_page()
  pdf.set_font('montserrat', size=32)
  pdf.cell(80)
  pdf.cell(w=40, txt='Animotions',ln=1,border=1)
  pdf.set_font('montserrat', size=16)
  pdf.cell(w=40, txt='beyond the visual',ln=1,border=1)
  pdf.set_font('Arial', size=14)
  pdf.cell(w=40, txt='www.animotions.be',ln=1)
  project_name = input("Type in the project name: ")

  pdf.add_page()
  pdf.cell(80)
  pdf.cell(80,txt=project_name)
  pdf.set_font('Arial', 'B', size=16)


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

  files = [x for x in os.listdir(pov) if "CAM" in x]
  for f in files:
    pdf.add_page()
    camname = os.path.splitext(f)[0]
    pdf.cell(w=40,h=0, txt=project_name, align='L', ln=1)
    pdf.cell(w=40,h=10,txt=camname, align='L')
    
  mv = os.path.join(cwd, 'MV')

  mvs = [int(x[0:1]) for x in os.listdir(mv)]

  print(max(mvs))

  datum = date.today().strftime("%Y%m%d")
  pdf.output(os.path.join(mv, f'{max(mvs)+1}_{datum}_pov_brief.pdf'), 'F')




  
