from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/zhs_tours'  # Replace with your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    person = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)

# Route to handle login and session management
@app.route('/')
def index():
    if 'name' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    return render_template('dashboard.html', name=session.get('name'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement authentication logic here
        session['name'] = username  # Placeholder
        return redirect('/')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name', None)
    flash("Logged out successfully!", "success")
    return redirect('/login')

@app.route('/add-package', methods=['GET', 'POST'])
def add_package():
    if 'name' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            destination = request.form['destination']
            duration = request.form['duration']
            person = int(request.form['person'])
            price = float(request.form['price'])
            description = request.form['description']

            # Handle file upload
            file = request.files['uploadfile']
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
            else:
                flash("Failed to upload file", "error")
                return redirect('/add-package')

            # Save package data to database
            new_package = Package(
                country=destination,
                duration=duration,
                person=person,
                price=price,
                description=description,
                image=filepath
            )
            db.session.add(new_package)
            db.session.commit()
            flash("Package added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding package: {e}", "error")
        return redirect('/add-package')

    return render_template('add_package.html')

@app.route('/packages')
def show_packages():
    if 'name' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    packages = Package.query.all()
    return render_template('packages.html', packages=packages)

@app.route('/delete-package/<int:id>', methods=['POST'])
def delete_package(id):
    if 'name' not in session:
        flash("Please login first!", "error")
        return redirect('/login')

    package = Package.query.get_or_404(id)
    try:
        if os.path.exists(package.image):
            os.remove(package.image)
        db.session.delete(package)
        db.session.commit()
        flash("Package deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting package: {e}", "error")
    return redirect('/packages')
if __name__ == '__main__':
    app.run(debug=True)
