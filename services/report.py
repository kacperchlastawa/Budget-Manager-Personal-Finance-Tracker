import os
import tempfile
import smtplib
from email.message import EmailMessage
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from config.email_config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
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
        self.elements.append(Paragraph(text, self.title_style))
        self.elements.append(Spacer(1,20))

    def add_subtitle(self,text):
        self.elements.append(Paragraph(text,self.subtitle_style))
        self.elements.append(Spacer(1,10))
    
    def add_paragraph(self,text):
        self.elements.append(Paragraph(text, self.styles["Normal"]))
        self.elements.append(Spacer(1,12))

    def add_table(self,df, caption = None):
        if df.empty:
            self.add_paragraph("Brak danych do wyświetlenia.")
            return
        data = [df.columns.tolist()] + df.values.tolist()
        col_count = len(df.columns)
        col_width = 450 / col_count
        table = Table(data, hAlign = "LEFT", colWidths=[col_width] * col_count)
        table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("BACKGROUND", (0,0),(-1,0),colors.lightblue),
            ("TEXTCOLOR", (0,0),(-1,0), colors.black),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0),(-1,-1), 0.5, colors.lightseagreen),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4)
        ]))
        self.elements.append(table)
        if caption:
            self.elements.append(Paragraph(caption,self.styles["Italic"]))
        self.elements.append(Spacer(1,8))



    def add_figure(self, fig, caption = None, width = None, height = None):
        if fig is None:
            self.add_paragraph("No chart to display.")
            return
        if caption:
            self.elements.append(Paragraph(caption, self.styles["Italic"]))
        temp = tempfile.NamedTemporaryFile(delete=False,suffix=".png")
        fig.savefig(temp.name,bbox_inches='tight')
        plt.close(fig)
        self.temp_files.append(temp.name)
        self.elements.append(Image(temp.name, width, height))
        self.elements.append(Spacer(1,12))


    def add_page_break(self):
        self.elements.append(PageBreak())

    def add_timestamp(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.elements.append(Paragraph(f"Raport generated: {now}", self.styles["Normal"]))
        self.elements.append(Spacer(1,12))
    def save_temp_report(self, filename = None):
        if not filename:
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            filename = temp.name

        doc = SimpleDocTemplate(filename, pagesize = self.pagesize)
        doc.build(self.elements)
        for f in self.temp_files:
            os.remove(f)
        return filename
        
    def export_to_email(self, address):
        temp_report = os.path.join(os.getcwd(), "temp_report.pdf")      
        with open(self.filename, "rb") as src, open(temp_report, "wb") as dst:
            dst.write(src.read())
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = address
            msg['Subject'] = "Your Budget Report"

            msg.attach(MIMEText("Please find attached your budget report.", 'plain'))
            with open(temp_report, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="pdf") 
                part.add_header("Content-Disposition", "attachment", filename=os.path.basename(temp_report))
                msg.attach(part)

            smtp_server = SMTP_SERVER
            smtp_port = SMTP_PORT
            sender_email = EMAIL_SENDER
            sender_password = EMAIL_PASSWORD
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)


            print("✅ Report sent successfully!")

        except Exception as e:
            print(f"❌ Failed to send email: {e}")

        finally:
            if os.path.exists(temp_report):
                os.remove(temp_report)

        
    def build(self):
        try:
            doc = SimpleDocTemplate(self.filename, pagesize = self.pagesize)
            doc.build(self.elements)
        finally:
            self._cleanup_temp_files()
    def _cleanup_temp_files(self):
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception as e:
                print(f"Warning: Could not remove {f}: {e}")
        self.temp_files.clear()
