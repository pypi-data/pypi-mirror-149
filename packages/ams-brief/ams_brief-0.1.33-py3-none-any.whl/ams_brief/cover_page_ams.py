cover_logo = "X:/9999_BID_AMS/AMS_Logo's/RGB/Animotions_Logo_02_Neg_RGB.png"


def create_cover_page(brief):
    brief.add_page()
    brief.set_fill_color(224, 157, 157)
    brief.set_text_color(60, 60, 60)
    brief.set_font('montserrat', size=48)
    brief.rect(x=10, y=10, w=275, h=190, style='F')
    #brief.set_xy(20, 100)
    brief.image(cover_logo, x=20, y=100, w=50)
    #brief.cell(w=0, txt='ANIMOTIONS', ln=2)
    brief.set_xy(20, 110)
    brief.set_font('nexa', size=16)
    brief.cell(w=0, txt='beyond the visual')
    brief.set_xy(20, 185)
    brief.set_font('nexa', size=14)
    brief.cell(0, txt='www.animotions.be')
