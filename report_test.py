from services.data_analyzer import *
from services.report import * 
from services.visualization import * 

report = Report(filename='budget_raport.pdf',pagesize=A4) 

piechart_category = plot_transactions_by_category(get_transactions_by_category())
balance_chart = balance_over_time(get_balance_over_time(period = 'daily'), period = 'daily')
income_vs_expense_chart = plot_incomes_vs_expenses(get_income_vs_expense(limit=5))
top_expenses_chart = plot_top_n_expenses(get_top_expenses(limit=5))
chart_savings_progress = plot_savings_progress(get_savings_progress())
summary = get_monthly_summary(2025, 10)
summary_table = pd.DataFrame([summary])  # <- konwersja słownika na DataFrame
summary2 = get_monthly_summary(2025,9)
summary_table2 = pd.DataFrame([summary2])
# -----------------------
# STRONA 1 — TYTUŁ + META
# -----------------------
report.add_title("Budget report — October 2025")
report.add_timestamp()
report.add_paragraph("This report shows financial summary of October 2025, including expenses, incomes and users savings analysis.")
report.add_page_break()

# -----------------------
# STRONA 2 — WYKRESY
# -----------------------
report.add_title("Data visualisation")
report.add_paragraph(" Charts below shows the most important personal budget indicators.")

report.add_figure(piechart_category, "Most common expenses", 280, 280)
report.add_figure(top_expenses_chart, "Top 5 biggest expenses", 250, 250)
report.add_figure(income_vs_expense_chart, "Incomes and expenses comparision", 300, 300)
report.add_figure(balance_chart, "change in balance- over time", 300, 300)
report.add_figure(chart_savings_progress, "Saving progress", 300, 300)

report.add_page_break()

# -----------------------
# STRONA 3 — PODSUMOWANIE
# -----------------------
report.add_title("Summary of the month")
report.add_paragraph("The table below shows key financial statistics for the current month:")

report.add_table(summary_table, "Tabel. October 2025 - summary")
report.add_table(summary_table2, "Tabel. September 2025 - summary")

# -----------------------
# BUDOWA RAPORTU
# -----------------------
report.build()

