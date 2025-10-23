import schedule,time
from datetime import datetime
from data_analyzer import get_monthly_summary

def daily_budget_check():
    summary = get_monthly_summary(datetime.now().year,datetime.now().month)
    if summary['total_expenses'] > summary['budget']:
        print("Alert: You have exceeded your budget for this month!")
def run_scheduler():
    schedule.every().day.at("09:00").do(daily_budget_check)
    while True:
        schedule.run_pending()
        time.sleep(60)
if __name__ == "__main__":
    run_scheduler()







