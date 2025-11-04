# 💰 Budget Manager — Personal Finance App

Budget Manager is a complete personal finance management system built with **Python** and **Streamlit**. It is designed to help users track expenses, manage savings, and generate insightful monthly reports—all in one place.

---

## ✨ Application Preview (Demo)

**login page**

<img width="1164" height="756" alt="image" src="https://github.com/user-attachments/assets/0cc66258-96e5-4090-a46f-351a54ee4e28" />


**main page**
<img width="1569" height="909" alt="image" src="https://github.com/user-attachments/assets/078cee54-c554-4975-a0a9-6193357795b4" />

**Budget section**

   * Adding income/expense - here we can add both income and expense
     
     <img width="1550" height="640" alt="image" src="https://github.com/user-attachments/assets/152ed83e-b0f0-4402-93b1-9b1fbb5fca0b" />
     
   * Displaying transactions - here we can choose number of transactons we want to see and option From beginning/ From the end

        <img width="1536" height="555" alt="image" src="https://github.com/user-attachments/assets/d5267fac-b791-4c5f-a2f5-888883066e73" />

     
   * Here we can filter transactions by category
     
        <img width="1566" height="743" alt="image" src="https://github.com/user-attachments/assets/44480922-2422-4313-ac63-23735df7909c" />
   
   * Filtering transactions by type (income/expense)

       <img width="1544" height="253" alt="image" src="https://github.com/user-attachments/assets/c168914d-608a-4f85-8775-77612821e07c" />

   * Here we can calculate sum of all incomes or expenses

        <img width="1823" height="610" alt="image" src="https://github.com/user-attachments/assets/34207291-5fc8-4607-823c-4e551238a386" />
     

**Savings section**

   * At the beginning we can add goal and set the goal amount or remove the goal.

       <img width="1520" height="328" alt="image" src="https://github.com/user-attachments/assets/a517acde-e4ad-477a-adda-233ade02ce17" />
       
  * We can display all our saving goals:

     <img width="1522" height="669" alt="image" src="https://github.com/user-attachments/assets/4195e1af-7d9a-460f-85e4-15f17465ca69" />

    * We can add money from budget to our goal:

      <img width="1522" height="669" alt="image" src="https://github.com/user-attachments/assets/e774dcb4-2a31-4a8e-bada-ac67fd70796c" />
      
     * Or we can withdraw the money from it:

         <img width="1522" height="669" alt="image" src="https://github.com/user-attachments/assets/6e737189-acde-43be-98a0-f28dfc573228" />


  **Report section**
  
  In this section you can generate pdf with monthly summary, showing different charts and budget analysis. You can also export it to an email.

      <img width="1796" height="845" alt="image" src="https://github.com/user-attachments/assets/277216b1-cae9-403d-a918-3bbb4ecbf6ee" />

  
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

## 🚀 Features

* **✅ User Authentication** — Secure registration & login.
* **✅ Expense & Income Tracking** — Add, edit, filter and search through transactions with category support.
* **✅ Savings Goals** — Set and monitor progress toward financial goals.
* **✅ Interactive Visualizations** — Charts for spending distribution, income vs. expenses, and savings trends.
* **✅ Reports** — Generate monthly PDF summaries with visual data and analytics.
* **✅ Email Alerts** — Automatic notifications when spending exceeds income.
* **✅ Daily Automation** — Background scheduler to run daily budget checks.
* **✅ Streamlit Interface** — Modern, responsive UI with a clean sidebar and easy navigation.

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python 3.12
* **Database:** SQL Server (via `pyodbc`)
* **Reports:** ReportLab (PDF generation)
* **Automation:** `schedule` (daily background jobs)
* **Visualization:** Matplotlib / Pandas
* **Email Integration:** SMTP (Gmail App Password)


---

## ⚙️ How It Works

1.  **Login or Register** — Users create personal accounts; all data is separated per user.
2.  **Add Transactions** — Log daily expenses and incomes by category.
3.  **Track Progress** — Visualize spending and savings trends interactively.
4.  **Generate Reports** — Produce professional monthly PDF summaries.
5.  **Automation** — A background scheduler checks every morning for overspending.
6.  **Email Alerts** — Sends warnings and summary reports automatically.

### 🛡️ Security

* Passwords are securely **hashed** using `Werkzeug`.
* App passwords or tokens are stored outside the repository in `config/email_config.py` (which is excluded from Git via `.gitignore`).

---

## 🧑‍💻 Autohr

**Kacper Chlastawa**
* Applied Computer Science student

### 📬 Contact

* **📧 Email:** [kacper.chlastawa03@gmail.com]
* **🌐 GitHub:** [github.com/kacperchlastawa]
