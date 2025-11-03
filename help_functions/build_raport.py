from services.report import Report
from services.data_analyzer import *
from services.visualization import *
from datetime import datetime
from reportlab.lib.pagesizes import A4
from calendar import month_name
import os
import pandas as pd

def build_raport(filename, month, year):
        output_path = os.path.abspath(filename)

        report = Report(output_path, pagesize=A4)
        report.add_title(f"Budget Report — {month_name[month]} {year}")
        report.add_timestamp()
        report.add_paragraph(f"This report shows financial summary of {datetime(year, month, 1).strftime('%B %Y')}, including expenses, incomes and users savings analysis.")
        report.add_title("Data visualisation")
        report.add_paragraph(" Charts below shows the most important personal budget indicators.")
        piechart_category = plot_transactions_by_category(get_transactions_by_category(month,year))

        report.add_figure(piechart_category, "Most common expenses", 280, 280)
        report.add_paragraph("The pie chart above illustrates the distribution of expenses across various categories, providing insights into spending habits.")

        balance_chart =balance_over_time(get_balance_over_time(period = 'daily'), period = 'daily')
        balance_chart_2 = balance_over_time(get_balance_over_time(period = 'monthly'), period = 'monthly')
        report.add_figure(balance_chart, "Change in balance - daily", 300, 300)
        report.add_paragraph("The line chart above depicts the daily changes in your account balance over time, highlighting trends and fluctuations.")
        report.add_figure(balance_chart_2, "Change in balance - monthly", 300, 300)
        report.add_paragraph("The line chart above illustrates the monthly changes in your account balance, providing a broader perspective on financial trends.")

        income_vs_expense_chart = plot_incomes_vs_expenses(get_income_vs_expense(limit=5))
        report.add_figure(income_vs_expense_chart, "Incomes and expenses comparison", 300, 300)
        report.add_paragraph("The bar chart above compares your monthly incomes and expenses, allowing you to visualize your financial balance.")

        top_expenses_chart = plot_top_n_expenses(get_top_expenses(limit=5, year=year, month=month))
        report.add_figure(top_expenses_chart, "Top 5 biggest expenses", 250, 250)
        report.add_paragraph("The horizontal bar chart above highlights your top 5 biggest expenses, helping you identify major spending areas.")

        chart_savings_progress = plot_savings_progress(get_savings_progress())
        report.add_figure(chart_savings_progress, "Saving progress", 300, 300)
        report.add_paragraph("The area chart above illustrates your savings progress over time, showcasing how your savings have accumulated.")

        summary = get_monthly_summary(year, month)
        summary_table = pd.DataFrame([summary])  
        summary2 = get_monthly_summary(year, month-1 if month > 1 else 12)
        summary_table2 = pd.DataFrame([summary2])
        report.add_title("Summary of the month")
        report.add_paragraph("The table below shows key financial statistics for the current month:")
        report.add_table(summary_table, f"Table. {datetime(year, month, 1).strftime('%B %Y')} - summary")
        report.add_paragraph("The table above provides a detailed summary of your financial statistics for the selected month, including total income, expenses, and balance.")
        if summary2 is not None:
            report.add_table(summary_table2, f"Table. {datetime(year, month-1 if month > 1 else 12, 1).strftime('%B %Y')} - summary")
            report.add_paragraph("The table above provides a detailed summary of your financial statistics for the previous month, allowing for comparison with the current month.")
        report.build()
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise FileNotFoundError(f"Report file was not created correctly at {output_path}")

        return report