## 📊 Payment Discrepancy Resolution System

### 🔹 Overview

This project automates invoice vs. payment mismatch detection using PostgreSQL, Python, Streamlit, and Email Alerts. It helps businesses identify underpaid and overpaid invoices, generate reports, and send automated alerts.

###🔹 Features

✅ Automated Data Extraction (PostgreSQL + Python)

✅ Invoice vs Payment Mismatch Detection

✅ Dynamic Dashboard with Filters (Streamlit)

✅ Automated Email Alerts with Reports (Gmail SMTP)

✅ CSV & Excel Report Downloads

✅ Data Visualizations with Seaborn & Matplotlib


### 🔹 Tech Stack

Backend: PostgreSQL, Python (psycopg2 for database connection)

Frontend: Streamlit (Interactive Web Dashboard)

Data Processing: Pandas, Matplotlib, Seaborn

Automation: SMTP Email Integration (Gmail)

Deployment: Local Execution via streamlit run app.py


### 1️⃣ Setup & Installation

📌 Step 1: Clone the Repository

git clone https://github.com/DataFinFreak/payment-discrepancy-system.git
cd payment-discrepancy-system

📌 Step 2: Install Dependencies

pip install -r requirements.txt

📌 Step 3: Set Up PostgreSQL Database

Install PostgreSQL (Download Here)


### Create a new database:

CREATE DATABASE Payment_Discrepancy_Resolution_System;


### Create Tables:

CREATE TABLE Invoices (
    invoice_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Unpaid'
);

CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    invoice_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id) ON DELETE CASCADE
);

### Load sample data from CSV:

psql -U postgres -d Payment_Discrepancy_Resolution_System -c "\copy Invoices FROM 'invoices.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d Payment_Discrepancy_Resolution_System -c "\copy Payments FROM 'payments.csv' DELIMITER ',' CSV HEADER;"


### 2️⃣ Running the Application

📌 Step 1: Run the Streamlit Dashboard

streamlit run app.py

📌 Step 2: Test Email Alerts

Set up Gmail App Passwords (Guide).

Modify .env file to include:

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

Run the script:

python send_email.py


### 3️⃣ Screenshots

📊 Dashboard View

![Image](https://github.com/user-attachments/assets/bad31f55-66e1-41d6-bd40-632c07183515)

![Image](https://github.com/user-attachments/assets/b3ff75e9-242d-41e8-b5a6-4638812fda5c)

📧 Email Alert Example

![Image](https://github.com/user-attachments/assets/fc326d2f-113c-4d4f-b5d5-e6d44dbc0648)

![Image](https://github.com/user-attachments/assets/8c4f2902-b26b-4e91-aa0b-cb9fba106dce)


### 4️⃣ Contributing

Want to improve this project? Feel free to fork and submit a pull request!

Youtube - https://youtu.be/3PWY-E3Ung8

### 5️⃣ License

This project is licensed under the MIT License - see the LICENSE file for details.

🚀 Happy Coding!
