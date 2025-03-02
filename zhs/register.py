from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

db_config = {
    'host': 'localhost',
    'user': 'root',         # Replace with your MySQL username
    'password': '', # Replace with your MySQL password
    'database': 'zhs_data'
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('user')
        email = request.form.get('mail')
        password = request.form.get('pass')

        try:
            # Connect to the database
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Insert data into the 'users' table
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            connection.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('register'))

        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('register.html')  # Render your registration HTML file

if __name__ == '__main__':
    app.run(debug=True)
