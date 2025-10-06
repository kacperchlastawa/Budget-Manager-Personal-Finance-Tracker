from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import tempfile
import matplotlib.pyplot as plt


class Report:

    def __init__(self, filename  = 'budget_raport.pdf', pagesize=A4):
        self.filename = filename
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self.elements = []
        self.temp_files = [] 

        self.title_style = ParagraphStyle(
            name="Title",
            parent=self.styles["Heading1"],
            alignment=TA_CENTER,
            fontSize=20,
            spaceAfter=20
        )
        self.subtitle_style = ParagraphStyle(
            name="Subtitle",
            parent=self.styles["Heading2"],
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            spaceAfter=10
        )
    def add_title(self,text):
        pass

    def add_subtitle(self,text):
        pass
    
    def add_paragraph(self,text):
        pass

    """dla funkcji month_summary z data_analyzer"""
    def add_table(self,df, caption = None):
        pass

    def add_figure(self, fig, caption = None, width = None, height = None):
        pass

    def add_page_break(self):
        pass

    def add_header_footer(self, header_text, footer_text):
        pass

    def save_temp_report(self, filename = None):
        pass

    def export_to_email(self, address):
        pass
    def build(self):
        pass