# Manpower Management System

## Project Overview

The Manpower Management System is a Flask-based web application designed to streamline the management of employee documents, events, and requests. It provides a centralized platform for tracking important information, scheduling events, and handling internal requests, ensuring efficient operations and compliance.

## Features

* **Document Management**: Upload, view, edit, and delete various employee documents (Iqama, License, Muqeem, Sabic ID, Aramco ID, Ajeer, etc.) with expiry date tracking.
* **Event Calendar**: A calendar view to add and manage important events.
* **Request Submission**: Users can submit detailed requests through a dedicated form.
* **Admin Panel for Requests**: A password-protected admin interface to view and delete submitted requests.
* **Search Functionality**: Easily search for employee documents by name or Iqama number.
* **Consistent Navigation**: A unified navigation bar across all pages for a smooth user experience.
* **Email Notifications**: (Implied by `smtplib` in `app.py`, though not fully implemented in provided snippets, it's a potential feature).

## Technologies Used

* **Backend**: Python, Flask, Flask-SQLAlchemy
* **Database**: SQLite
* **Frontend**: HTML5, CSS3 (custom styling), Jinja2 (templating)
* **Other**: Werkzeug (for file uploads)

## Installation

To get this project up and running on your local machine, follow these steps:

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone <your-repository-url>
cd manpowermanagement-
```

*(Replace `<your-repository-url>` with the actual URL of your GitHub repository)*

### 2. Set up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install Flask Flask-SQLAlchemy Werkzeug
```

### 4. Initialize the Database

The application uses SQLite. The database file (`documents.db`) will be created automatically when you run the application for the first time, thanks to `db.create_all()` in `app.py`.

### 5. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application should now be running at `http://127.0.0.1:5000/`.

## Usage

* **Home Page (`/`)**: Redirects to `/home`, a simple landing page.
* **Add Document (`/add_document`)**: Submit new employee documents with various details and file uploads.
* **View or Edit Document (`/search`)**: Search for existing documents and navigate to view or edit them.
* **All Entries (`/all_documents`)**: View a list of all submitted documents.
* **Calendar (`/calendar`)**: View and add events to a calendar.
* **Add Request (`/add_request`)**: Submit a new request.
* **Admin (`/admin_requests`)**: Access the password-protected admin panel to view and delete requests. The default admin password is `admin`.

## Project Structure
# HR-training-calender
