import os
from datetime import date
from pathlib import Path
import webbrowser

import click

from fpdf import FPDF
import imagesize

from .cover_page_ams import create_cover_page
from .cover_page_project import create_project_cover
from .directory import get_images
from .mv import create_mv_folder
from .functions import get_client_and_project, get_date, get_project_number

font_dir = Path('X:/9999_BID_AMS/AMS-VFB_Fonts')

logo = "X:/9999_BID_AMS/AMS_Logo's/RGB/Animotions_Logo_02_RGB.png"

frame_width = 200
frame_height = 170


def get_cwd():
    cwd = os.getcwd()
    if cwd[0] != 'X':
        click.secho("Please run the tool in the X:/ drive")
        return None

    if len(cwd) == 3:
        click.secho('Please run tool inside a project folder')
        return None

    return cwd


def main():
    click.echo(f"🥰 Let's create a briefing {os.getlogin()}!")
    pdf = FPDF(orientation='L', format='A4')
    pdf.set_author('Animotions')
    pdf.set_creator(os.getlogin())
    pdf.add_font(family='montserrat',
                 fname=font_dir.joinpath("Montserrat-ExtraBold.ttf"),
                 uni=True)

    pdf.add_font(family='nexa',
                 fname=font_dir.joinpath('Nexa Regular Italic.ttf'),
                 uni=True)

    project_path = Path(get_cwd())

    if project_path is None:
        return

    click.echo(f"🕵️‍♀️ We're running in {str(project_path)}")

    selection = get_images(project_path)

    project_name = input("🙏 Type in the project name: ")

    create_cover_page(pdf)
    create_project_cover(pdf, project_name)
    pdf.set_subject(project_name)
    pdf.set_title(f"Briefing - {project_name}")

    proj_number = get_project_number(project_path)

    if len(proj_number) != 4:
        click.secho('probber')

    files = [x for x in selection.iterdir() if x.is_file()
             and x.suffix == ".jpg"]
    for f in files:
        pdf.add_page()
        camname = f.stem.replace('_', ' ')
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

    mv_dir = create_mv_folder(project_path, verbose=True)

    dest = mv_dir.joinpath(
        f'{get_date()}_{get_client_and_project(project_path)}_briefing.pdf')
    pdf.output(dest, 'F')
    webbrowser.open(dest)
