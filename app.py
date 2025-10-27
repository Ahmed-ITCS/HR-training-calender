from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'null'
app.config['SESSION_PERMANENT'] = False
app.secret_key = 'your_secret_key'  # Replace with a strong, unique secret key

ADMIN_PASSWORD = 'admin'

db = SQLAlchemy(app)

# Email credentials
SENDER_EMAIL = "ahmedkhawarbs@gmail.com"
APP_PASSWORD = "oggv zthz rnlx dret"
RECIPIENT_EMAIL = "ahmedphp676@gmail.com"

# Document model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    iqama = db.Column(db.String(100), unique=True, nullable=False)
    iqama_expiry = db.Column(db.String(100), nullable=False)
    iqama_pic = db.Column(db.String(200), nullable=True)
    license = db.Column(db.String(100), unique=True, nullable=False)
    license_expiry = db.Column(db.String(100), nullable=False)
    licensepicture = db.Column(db.String(200), nullable=True)
    Muqeempicture = db.Column(db.String(200), nullable=True)
    MuqeemExpiry = db.Column(db.String(100), nullable=False)


    Sabicid = db.Column(db.String(100), unique=True, nullable=False)
    Sabicidpicture = db.Column(db.String(200), nullable=True)
    SabicExpiry = db.Column(db.String(100), nullable=False)

    Aramcoid = db.Column(db.String(100), unique=True, nullable=False)
    Aramcoidpicture = db.Column(db.String(200), nullable=True)
    AramcoidExpiry = db.Column(db.String(100), nullable=False)

    Sabicmedicalpicture = db.Column(db.String(200), nullable=True)
    SabicmedicalExpiry = db.Column(db.String(100), nullable=False)

    Ajeerpicture = db.Column(db.String(200), nullable=True)
    AjeerExpiry = db.Column(db.String(100), nullable=False)

    other1 = db.Column(db.String(200), nullable=True)
    other1expiry = db.Column(db.String(100), nullable=False)

    other2 = db.Column(db.String(200), nullable=True)
    other2expiry = db.Column(db.String(100), nullable=False)

    other3 = db.Column(db.String(200), nullable=True)
    other3expiry = db.Column(db.String(100), nullable=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    request_details = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    selected_date = request.args.get('date')
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        description = request.form['description']
        new_event = Event(date=date, title=title, description=description)
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('view_events', date=date))
    return render_template('add_event.html', selected_date=selected_date)

@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        request_details = request.form['request_details']
        new_request = Request(name=name, email=email, request_details=request_details)
        db.session.add(new_request)
        db.session.commit()
        flash('Your request has been submitted successfully!', 'success')
        return redirect(url_for('index')) # Redirect to home or a confirmation page
    return render_template('add_request.html')

@app.route('/view_events/<date>')
def view_events(date):
    events = Event.query.filter_by(date=date).all()
    return render_template('view_events.html', date=date, events=events)

@app.route('/add_document', methods=['GET'])
def add_document():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    iqama = request.form.get('iqama')
    iqama_expiry = request.form.get('iqama_expiry')
    license = request.form.get('license')
    license_expiry = request.form.get('license_expiry')
    sabicid = request.form.get('Sabicid')
    aramcoid = request.form.get('Aramcoid')

    MuqeemExpiry = request.form.get('MuqeemExpiry')
    SabicExpiry = request.form.get('SabicExpiry')
    AramcoidExpiry = request.form.get('AramcoidExpiry')
    SabicmedicalExpiry = request.form.get('SabicmedicalExpiry')
    AjeerExpiry = request.form.get('AjeerExpiry')

    other1expiry = request.form.get('other1expiry')
    other2expiry = request.form.get('other2expiry')
    other3expiry = request.form.get('other3expiry')

    uploaded_files = {}
    for field in ['iqamapicture', 'licensepicture', 'Muqeempicture', 'Sabicidpicture',
                  'Aramcoidpicture', 'Sabicmedicalpicture', 'Ajeerpicture',
                  'other1picture', 'other2picture', 'other3picture']:
        file = request.files.get(field)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_files[field] = "uploads/" + filename  # Store only the filename
        elif file:
            return render_template('index.html', message="File type not allowed")

    document = Document(
        name=name,
        iqama=iqama,
        iqama_expiry=iqama_expiry,
        license=license,
        license_expiry=license_expiry,
        Sabicid=sabicid,
        Aramcoid=aramcoid,
        iqama_pic=uploaded_files.get('iqamapicture'),
        licensepicture=uploaded_files.get('licensepicture'),
        Muqeempicture=uploaded_files.get('Muqeempicture'),
        Sabicidpicture=uploaded_files.get('Sabicidpicture'),
        Aramcoidpicture=uploaded_files.get('Aramcoidpicture'),
        Sabicmedicalpicture=uploaded_files.get('Sabicmedicalpicture'),
        Ajeerpicture=uploaded_files.get('Ajeerpicture'),
        other1=uploaded_files.get('other1picture'),
        other2=uploaded_files.get('other2picture'),
        other3=uploaded_files.get('other3picture'),
        MuqeemExpiry=MuqeemExpiry,
        SabicExpiry=SabicExpiry,
        AramcoidExpiry=AramcoidExpiry,
        SabicmedicalExpiry=SabicmedicalExpiry,
        AjeerExpiry=AjeerExpiry,
        other1expiry=other1expiry,
        other2expiry=other2expiry,
        other3expiry=other3expiry,
    )

    db.session.add(document)
    db.session.commit()
    return render_template('index.html', message="Submitted successfully!")
    ##flash("Document submitted successfully!")
    ##return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    names = Document.query.with_entities(Document.name, Document.iqama).all()  # Fetch names & Iqamas

    if request.method == 'POST':
        iqama = request.form.get('Iqama')
        document = Document.query.filter_by(iqama=iqama).first()
        if document:
            return redirect(url_for('view_document', doc_id=document.id))
            #return redirect(url_for('view', document=document))  # Corrected line
        else:
            return render_template('search.html', names=names, message="No document found")

    return render_template('search.html', names=names)


@app.route('/view/<int:doc_id>', methods=['GET'])
def view_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    return render_template('view.html', document=document)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_document(id):
    document = Document.query.get_or_404(id)
    if request.method == 'POST':
        document.name = request.form['name']
        document.iqama = request.form['iqama']
        document.iqama_expiry = request.form['iqama_expiry']
        document.license = request.form['license']
        document.license_expiry = request.form['license_expiry']

        document.MuqeemExpiry = request.form['MuqeemExpiry']
        document.SabicExpiry = request.form['SabicExpiry']
        document.AramcoidExpiry = request.form['AramcoidExpiry']
        document.SabicmedicalExpiry = request.form['SabicmedicalExpiry']
        document.AjeerExpiry = request.form['AjeerExpiry']

        for field in ['iqamapicture', 'licensepicture']:
            file = request.files.get(field)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                setattr(document, field, file_path)

        db.session.commit()
        return redirect(url_for('view_document', doc_id=document.id))

    return render_template('edit.html', document=document)

@app.route('/all_documents')
def all_documents():
    documents = Document.query.all()
    return render_template('all.html', documents=documents)

@app.route('/admin_requests', methods=['GET', 'POST'])
def admin_requests():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Logged in as admin!', 'success')
        else:
            flash('Incorrect password.', 'error')
        return redirect(url_for('admin_requests'))

    if not session.get('admin_logged_in'):
        return render_template('admin_requests.html')

    requests = Request.query.order_by(Request.timestamp.desc()).all()
    return render_template('admin_requests.html', requests=requests)

@app.route('/delete_request/<int:request_id>', methods=['GET'])
def delete_request(request_id):
    if not session.get('admin_logged_in'):
        flash('Unauthorized access.', 'error')
        return redirect(url_for('admin_requests'))

    request_to_delete = Request.query.get_or_404(request_id)
    db.session.delete(request_to_delete)
    db.session.commit()
    flash('Request deleted successfully!', 'success')
    return redirect(url_for('admin_requests'))

@app.route('/delete/<int:doc_id>', methods=['GET'])
def delete_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('all_documents'))

if __name__ == '__main__':
    app.run(debug=True)
