import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# --- Setup Flask + DB (reuse existing DB and model) ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://instance/documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Document Model (same as app.py) ---
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    iqama = db.Column(db.String(100), unique=True, nullable=False)
    iqama_expiry = db.Column(db.String(100), nullable=False)
    license = db.Column(db.String(100), unique=True, nullable=False)
    license_expiry = db.Column(db.String(100), nullable=False)
    MuqeemExpiry = db.Column(db.String(100), nullable=False)
    SabicExpiry = db.Column(db.String(100), nullable=False)
    AramcoidExpiry = db.Column(db.String(100), nullable=False)
    SabicmedicalExpiry = db.Column(db.String(100), nullable=False)
    AjeerExpiry = db.Column(db.String(100), nullable=False)
    other1expiry = db.Column(db.String(100), nullable=False)
    other2expiry = db.Column(db.String(100), nullable=False)
    other3expiry = db.Column(db.String(100), nullable=False)

# --- Email Settings ---
SENDER_EMAIL = "ahmedkhawarbs@gmail.com"
APP_PASSWORD =  # <-- put your app password here
RECIPIENT_EMAIL = "ahmedphp676@gmail.com"

# --- Helper: Parse date safely ---
def parse_date(date_str):
    """Try to parse a date from string (supports multiple formats)."""
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

# --- Main Logic ---
def check_expiring_documents():
    today = datetime.now().date()
    threshold = today + timedelta(days=15)
    expiring_docs = []

    with app.app_context():
        documents = Document.query.all()
        for doc in documents:
            for field_name, expiry_value in {
                "Iqama": doc.iqama_expiry,
                "License": doc.license_expiry,
                "Muqeem": doc.MuqeemExpiry,
                "Sabic": doc.SabicExpiry,
                "Aramco": doc.AramcoidExpiry,
                "Sabic Medical": doc.SabicmedicalExpiry,
                "Ajeer": doc.AjeerExpiry,
                "Other1": doc.other1expiry,
                "Other2": doc.other2expiry,
                "Other3": doc.other3expiry,
            }.items():
                expiry_date = parse_date(expiry_value)
                if expiry_date and today <= expiry_date <= threshold:
                    expiring_docs.append({
                        "name": doc.name,
                        "type": field_name,
                        "expiry_date": expiry_date.strftime("%Y-%m-%d")
                    })

    return expiring_docs

# --- Email Sender ---
def send_email(expiring_docs):
    if not expiring_docs:
        print("No documents expiring soon. No email sent.")
        return

    subject = "⚠️ Documents Expiring in Next 15 Days"
    body = "The following documents are expiring soon:\n\n"
    for doc in expiring_docs:
        body += f"Name: {doc['name']} | Type: {doc['type']} | Expiry: {doc['expiry_date']}\n"
    body += "\nPlease take necessary action."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- Run ---
if __name__ == "__main__":
    expiring = check_expiring_documents()
    send_email(expiring)
