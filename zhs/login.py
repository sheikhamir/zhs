from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Replace with your MySQL password
    'database': 'zhs_data'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpass')

        try:
            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Query to check user credentials
            query = "SELECT * FROM users WHERE name = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                flash("Login successful!", "success")
                return redirect(url_for('index'))  # Redirect to index page
            else:
                flash("Invalid username or password. Please try again.", "danger")

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")

        finally:    
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')  # Serve the index page

if __name__ == '__main__':
    app.run(debug=True)

app=Flask(__name__,static_folder='static')
