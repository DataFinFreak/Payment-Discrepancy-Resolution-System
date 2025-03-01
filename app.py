import os
import psycopg2
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# ✅ Use environment variables for security
DB_NAME = os.getenv("DB_NAME", "Payment_Discrepancy_Resolution_System")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Manu@1999")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "ubdxgapunlkeiqhh")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "recipient@example.com")

# ✅ Database Connection & Data Fetching
def fetch_discrepancies():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        query = """
            SELECT i.invoice_id, i.customer_name, i.amount AS invoice_amount, 
                   COALESCE(SUM(p.amount), 0) AS total_paid, 
                   (i.amount - COALESCE(SUM(p.amount), 0)) AS discrepancy
            FROM Invoices i
            LEFT JOIN Payments p ON i.invoice_id = p.invoice_id
            GROUP BY i.invoice_id, i.amount
            HAVING i.amount != COALESCE(SUM(p.amount), 0);
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# ✅ Email Sending Function
def send_email_with_attachment(df):
    msg = EmailMessage()
    msg["Subject"] = "Payment Discrepancy Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content("Please find the attached discrepancy report.")
    
    # Convert DataFrame to Excel (in-memory)
    excel_data = BytesIO()
    df.to_excel(excel_data, index=False, engine='openpyxl')
    excel_data.seek(0)
    
    msg.add_attachment(
        excel_data.read(), maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="Discrepancy_Report.xlsx"
    )
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        st.success("✅ Email sent successfully!")
    except Exception as e:
        st.error(f"❌ Email sending failed: {e}")

# ✅ Streamlit Dashboard
def main():
    st.title("📊 Payment Discrepancy Dashboard")
    df = fetch_discrepancies()
    if df.empty:
        st.warning("No discrepancies found!")
        return
    
    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    customer_filter = st.sidebar.multiselect("Select Customer:", df["customer_name"].unique())
    amount_filter = st.sidebar.slider("Discrepancy Amount Range:", float(df["discrepancy"].min()), float(df["discrepancy"].max()))
    
    # Apply Filters
    if customer_filter:
        df = df[df["customer_name"].isin(customer_filter)]
    df = df[df["discrepancy"] <= amount_filter]
    
    # Display Data
    st.subheader("Filtered Discrepancies")
    st.dataframe(df)
    
    # Download Reports
    st.sidebar.markdown("### 📥 Download Reports")
    csv = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("Download CSV", csv, "filtered_discrepancies.csv", "text/csv")
    
    excel_data = BytesIO()
    df.to_excel(excel_data, index=False, engine='openpyxl')
    excel_data.seek(0)
    st.sidebar.download_button("Download Excel", excel_data, "filtered_discrepancies.xlsx")
    
    # Visualization
    st.subheader("📊 Discrepancy Analysis")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x="discrepancy", y="customer_name", palette="coolwarm", ax=ax)
    st.pyplot(fig)
    
    # Email Button
    if st.sidebar.button("📧 Send Email Report"):
        send_email_with_attachment(df)

if __name__ == "__main__":
    main()
