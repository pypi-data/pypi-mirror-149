import os
from datetime import date
from pathlib import Path

import click

from fpdf import FPDF
import imagesize

from .cover_page_ams import create_cover_page
from .cover_page_project import create_project_cover

font_dir = Path('X:/9999_BID_AMS/AMS-VFB_Fonts')

project_name = 'The South'
logo = "X:/9999_BID_AMS/AMS_Logo's/RGB/Animotions_Logo_02_RGB.png"

frame_width = 200
frame_height = 170


def get_cwd():
    cwd = os.getcwd()
    if cwd[0] != 'X':
        click.secho("Please run the tool in the X:/ drive")
        return

    if len(cwd) == 3:
        click.secho('Please run tool inside a project folder')
        return

    return cwd


def main():
    click.echo(f"🥰 Let's create a briefing {os.getlogin()}!")
    pdf = FPDF(orientation='L', format='A4')

    pdf.add_font(family='montserrat',
                 fname=font_dir.joinpath("Montserrat-ExtraBold.ttf"),
                 uni=True)

    pdf.add_font(family='nexa',
                 fname=font_dir.joinpath('Nexa Regular Italic.ttf'),
                 uni=True)

    create_cover_page(pdf)
    create_project_cover(pdf, project_name)

    # TODO remove hardcoded
    #project_dir = 'X:/1652_BTN_ZUI'

    project_path = Path(get_cwd())

    proj_number = str(project_path)[3:7]

    if len(proj_number) != 4:
        click.secho('probber')

    print(proj_number)

    stills = project_path.joinpath('Test_Stills')
    if not stills.is_dir():
        click.secho(
            f"You need a folder called 'Test_Stills' inside {str(project_path)}",
            fg='yellow')
        return

    pov = stills.joinpath("POV")

    if not pov.is_dir():
        click.secho(
            f"You need a folder called 'POV' inside {stills}",
            fg='yellow')
        return

    files = [x for x in pov.iterdir() if x.is_file()]
    for f in files:
        pdf.add_page()
        camname = f.stem
        pdf.set_font('Arial', 'B', size=18)
        pdf.cell(w=50, h=10, txt=project_name.upper(), align='R', ln=2)
        pdf.set_font('Arial', size=14)
        pdf.cell(w=50, h=10, txt=camname, align='R')
        pdf.image(logo, x=9, y=190, w=65)
        pdf.set_fill_color(200, 200, 200)
        pdf.rect(x=80, y=15, w=frame_width, h=frame_height, style='F')
        width, height = imagesize.get(str(f))

        ratio = width/frame_width

        ratio_y = height/ratio

        pdf.image(str(f), x=80, y=15+(frame_height - ratio_y)/2, w=200)

    mv = project_dir.joinpath('MV')

    # mvs = [int(x[0:1]) for x in os.listdir(mv)]

    # print(max(mvs))

    # datum = date.today().strftime("%Y%m%d")
    # dirname = os.path.join(mv, f'{max(mvs)+1}_{datum}_pov_brief')
    pdf.output(os.path.join(mv, 'pov_brief.pdf'), 'F')
