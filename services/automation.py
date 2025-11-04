import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import schedule
import time
from datetime import datetime
from services.data_analyzer import get_monthly_summary
from services.report import Report
from reportlab.lib.pagesizes import A4

def daily_budget_check(email):
    try:
        year = datetime.today().year
        month = datetime.today().month
        summary = get_monthly_summary(year, month)
        
        if summary and summary["total_exp"] > summary["total_income"]:
            print("⚠️ ALERT: Spending exceeds income this month!")
            
            report = Report(filename="alert_report.pdf", pagesize=A4)
            report.add_title("⚠️ Budget Alert Report")
            report.add_paragraph(
                f"Your expenses ({summary['total_exp']:.2f} zł) have exceeded your income ({summary['total_income']:.2f} zł) for {month}/{year}."
            )
            report.build()
            report.export_to_email(email)
            print(f"📧 Alert email sent to {email}")
        else:
            print("✅ Budget is fine, no alert needed.")
    except Exception as e:
        print(f"❌ Error in daily_budget_check: {e}")


def run_scheduler(user_email):
    schedule.every().day.at("09:00").do(daily_budget_check, email=user_email)
    print(f"⏰ Scheduler started for {user_email}... Press Ctrl+C to stop.")
    
    while True:
        schedule.run_pending()
        print(f"🕒 Scheduler tick at {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(180)

if __name__ == "__main__":
    daily_budget_check("your_email@example.com")
