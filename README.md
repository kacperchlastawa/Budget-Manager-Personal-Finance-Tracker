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
3. Install Dependencies

```bash
pip install -r requirements.txt
```
4. Configure Your Environment
You must configure your database connection and SMTP settings. See the "🔧 Configuration" section below.

5. Run the Application
The application is launched using Streamlit.
```bash
streamlit run ui/main_app.py
```

