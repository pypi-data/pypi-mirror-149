
def create_project_cover(brief, projectname):
    brief.add_page()
    brief.set_fill_color(252, 203, 181)
    brief.set_text_color(60, 60, 60)
    brief.set_font('Arial', 'B', size=32)
    brief.rect(x=10, y=10, w=275, h=190, style='F')
    brief.set_xy(20, 110)
    brief.cell(w=0, txt=projectname.upper())
    brief.set_xy(20, 185)
    brief.set_font('nexa', size=14)
    brief.cell(0, txt='www.animotions.be')
