from flask import Flask, render_template, request, redirect, url_for, flash
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

with app.app_context():
    db.create_all()

# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
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
@app.route('/delete/<int:doc_id>', methods=['GET'])
def delete_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('all_documents'))

if __name__ == '__main__':
    app.run(debug=True)
