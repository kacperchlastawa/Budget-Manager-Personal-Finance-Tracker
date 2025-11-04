import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import smtplib
from email.mime.text import MIMEText
from config.email_config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER,SMTP_PORT

def send_email(recipient, subject, body):
    """Generic helper to send email."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent successfully to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def send_budget_alert(email, month, year, total_exp, total_income):
    """Send alert when expenses exceed income."""
    body = (
        f"⚠️ Budget Alert!\n\n"
        f"Your expenses ({total_exp:.2f} zł) have exceeded your income ({total_income:.2f} zł) for {month}/{year}.\n"
        f"Please review your budget in the Budget Manager app."
    )
    send_email(email, "⚠️ Budget Alert - Spending Exceeded", body)

def send_big_expense_alert(email, category, amount):
    """Send alert when a single expense exceeds 1000 zł."""
    body = (
        f"💸 Big Expense Alert!\n\n"
        f"You've recorded a large expense of {amount:.2f} zł in category '{category}'.\n"
        f"Consider reviewing your spending plan to stay on track."
    )
    send_email(email, "💸 Big Expense Alert", body)

def send_savings_goal_progress(email, goal_name, progress):
    """Send alert when a savings goal reaches 90% or 100%."""
    if progress >= 1.0:
        subject = "🎉 Savings Goal Achieved!"
        body = (
            f"Congratulations! 🎯\n\n"
            f"You’ve reached 100% of your savings goal: '{goal_name}'. Great job achieving your target!"
        )
    elif progress >= 0.9:
        subject = "⏳ Almost There - Savings Goal 90% Reached!"
        body = (
            f"Keep going! 💪\n\n"
            f"You’ve reached {progress*100:.0f}% of your savings goal '{goal_name}'. You're very close to success!"
        )
    else:
        return  

    send_email(email, subject, body)