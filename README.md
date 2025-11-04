# 💰 Budget Manager — Personal Finance App

Budget Manager is a complete personal finance management system built with **Python** and **Streamlit**. It is designed to help users track expenses, manage savings, and generate insightful monthly reports—all in one place.

---

## ✨ Application Preview (Demo)

*(Insert a GIF or screenshot here demonstrating your application)*



---

## 🚀 Getting Started (Installation & Launch)

To run this application locally, follow the steps below.

### Prerequisites

Ensure you have the following installed:

* Python 3.10+
* Git
* Access to a SQL Server instance

### Installation

**1. Clone the Repository**


```bash
git clone https://github.com/kacperchlastawa/budget-manager.git
cd budget-manager
```
**2. Create and Activate a Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
**3. Install Dependencies**

```bash
pip install -r requirements.txt
```
**4. Configure Your Environment**
   
You must configure your database connection and SMTP settings. See the "🔧 Configuration" section below.

**5. Run the Application**

The application is launched using Streamlit.
```bash
streamlit run ui/main_app.py
```
---

## 🔧 Configuration

Before the first launch, the application requires key services to be configured.

### 1. Database (SQL Server)

The application requires a running SQL Server instance.

1.  Ensure your SQL Server instance is running.
2.  I recommend creating a dedicated database (e.g., `BudgetAppDB`).
3.  The application should automatically create the necessary tables on first run (based on the logic in `user_db.py`).
4.  Update the connection details in `data/connection.py` with your server, database name, and credentials.

> 🛡️ **Best Practice:** Do not include credentials in your code. Use environment variables (e.g., via a `.env` file and the `python-dotenv` library) to manage sensitive data securely.

### 2. Email Configuration (Gmail)

For the email alerts feature to work, you must configure the `config/email_config.py` file.

1.  This feature is designed to use a Gmail account.
2.  For security reasons, Gmail requires an **"App Password"** for third-party apps, not your regular account password.
3.  [Generate an "App Password"](https://support.google.com/accounts/answer/185833) by following Google's official guide.
4.  Place your email address and the 16-character generated password into `config/email_config.py`.

> ❗️ **Important:** Ensure that `config/email_config.py` (and any `.env` file) is added to your `.gitignore` file to avoid accidentally committing your credentials!

---

