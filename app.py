from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify, make_response
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os, time, MySQLdb.cursors
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)
# Encrypting "e7d97e15-ecff-416d-a618-dd7eb46e86bf" to SHA-256 to use as key
app.secret_key = 'a9aabe357b0f25b73d8915a4c7f706900605dcc7dbd86733f20ceccdd6008560'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'zhs'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `packages` ORDER BY `id` DESC LIMIT 0, 4")
    packages = cur.fetchall()
    cur.close()
    return render_template('home.html', logged_in=logged_in(), packages=packages)

# Admin routes
@app.route('/admin')
def dashboard():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Fetch number of bookings
    cur.execute("SELECT COUNT(*) as count FROM `bookings`")
    bookings = cur.fetchone()

    # Fetch number of tickets
    cur.execute("SELECT COUNT(*) as count FROM `airline_tickets`")
    tickets = cur.fetchone()

    # Fetch number of users
    cur.execute("SELECT COUNT(*) as count FROM `users`")
    users = cur.fetchone()

    # Fetch number of admins
    cur.execute("SELECT COUNT(*) as count FROM `admins`")
    admins = cur.fetchone()

    # Fetch number of packages
    cur.execute("SELECT COUNT(*) as count FROM `packages`")
    packages = cur.fetchone()

    # Fetch number of packages
    cur.execute("SELECT COUNT(*) as count FROM `custom_tours` where `status`='PENDING'")
    custom_tours = cur.fetchone()

    cur.close()

    data = {
        'bookings': bookings,
        'tickets': tickets,
        'users': users,
        'admins': admins,
        'packages': packages,
        'custom_tours': custom_tours
    }

    return render_template('admin/dashboard.html', data=data)

@app.route('/admin/bookings')
def bookings():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `bookings`")
    bookings = cur.fetchall()

    cur.execute("SELECT * FROM `tickets`")
    approved_bookings = cur.fetchall()

    # cur.execute("SELECT * FROM `custom_tours`")
    # custom_tours = cur.fetchall()
    cur.execute("""
        SELECT 
            GROUP_CONCAT(td.country) as country, 
            GROUP_CONCAT(tt.name) as people, 
            ct.id as id,
            ct.name as name,
            ct.email as email,
            ct.address as address,
            ct.details as details,
            ct.status as status,
            COUNT(DISTINCT td.id) AS total_tours, 
            COUNT(DISTINCT tt.id) AS total_people 
        FROM `custom_tours` ct
        JOIN `tour_destinations` td ON td.tour_id = ct.id
        LEFT JOIN `tour_travelers` tt ON tt.tour_id = ct.id
        GROUP BY ct.id
    """)
    custom_tours = cur.fetchall()
    
    cur.execute("SELECT * FROM `cancelled_bookings`")
    cancelled_bookings = cur.fetchall()

    cur.close()
    
    return render_template('admin/bookings.html', bookings=bookings, approved_bookings=approved_bookings, cancelled_bookings=cancelled_bookings, custom_tours=custom_tours)

@app.route('/admin/accept-booking/<int:id>', methods=['GET'])
def accept_booking(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))
        
        # Search for the package now
        cur.execute("SELECT * FROM packages WHERE country = %s", (booking['country'],))
        package = cur.fetchone()

        if not package:
            flash('Package not found!', 'danger')
            return redirect(url_for('bookings'))
        
        # Calculate price
        individual_per_day_price = package['price'] / package['person'] / package['duration']
        final_price = individual_per_day_price * booking['members'] * booking['days']

        # Insert the booking into the tickets table (approved bookings)
        query = """
            INSERT INTO tickets (name, email, package, price, deptr_date, contact, byuser)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (booking['name'], booking['email'], booking['country'], final_price, booking['travel_date'], booking['email'], booking['byuser']))  # Exclude the `id` field if not part of `tickets`
        mysql.connection.commit()

        # Delete the booking from the bookings table
        cur.execute("UPDATE bookings SET approved=1, status='USER_PAYMENT' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully accepted.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error accepting booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))
    
@app.route('/admin/mark-paid-booking/<int:id>', methods=['GET'])
def paid_booking(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE bookings SET status='PAID' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully accepted.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error accepting booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))
    
@app.route('/admin/ticketed-booking/<int:id>', methods=['GET'])
def ticketed_booking(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE bookings SET status='TICKET' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully accepted.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error accepting booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))

@app.route('/admin/cancel-booking/<int:id>', methods=['POST'])
def admin_cancel_booking(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking to ensure it exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()

        cancel_reason = request.form.get('cancel_reason')

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Insert data into the database
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO cancelled_bookings 
            (byuser, name, email, country, travel_date, members, days, hotel_type, flight_class, special_request, reason)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8], booking[9], booking[10], cancel_reason))
        #mysql.connection.commit()

        # Delete the booking from the bookings table
        cur.execute("DELETE FROM bookings WHERE id = %s", (id,))

        mysql.connection.commit()

        cur.close()

        flash('Booking successfully canceled.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error canceling booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))

@app.route('/admin/accept-custom-tour/<int:id>', methods=['GET'])
def custom_tour_user_payment(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM custom_tours WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE custom_tours SET status='CONFIRMED' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully accepted and awaiting payment.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error accepting booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))
    
@app.route('/admin/paid-custom-tour/<int:id>', methods=['GET'])
def custom_tour_paid(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM custom_tours WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE custom_tours SET status='PAID' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully marked as PAID.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error marking booking as paid: {str(e)}', 'danger')
        return redirect(url_for('bookings'))
    
@app.route('/admin/tickted-custom-tour/<int:id>', methods=['GET'])
def custom_tour_ticketed(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM custom_tours WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE custom_tours SET status='TICKET' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully marked as PAID and ticket generated.', 'success')
        return redirect(url_for('bookings'))

    except Exception as e:
        flash(f'Error generating ticket for booking: {str(e)}', 'danger')
        return redirect(url_for('bookings'))

@app.route('/admin/packages')
def view_packages():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `packages`")
    packages = cur.fetchall()
    cur.close()
    return render_template('admin/packages.html', packages=packages)

@app.route('/admin/packages/add', methods=['GET', 'POST'])
def add_packages():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Fetch form data
        destination = request.form.get('destination')
        duration = request.form.get('duration')
        person = request.form.get('person')
        price = request.form.get('price')
        description = request.form.get('description')
        file = request.files['uploadfile']

        # Validate inputs
        if not destination or not duration or not person or not price or not description or not file:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_packages'))
        
        # Allowed extensions
        allowed_extensions = {'jpg', 'bmp', 'webp', 'jpeg', 'png'}
        file_extension = file.filename.rsplit('.', 1)[-1].lower()

        if '.' not in file.filename or file_extension not in allowed_extensions:
            flash('Invalid file type! Please upload an image (jpg, bmp, webp, jpeg, png).', 'danger')
            return redirect(url_for('add_packages'))

        # Handle file upload
        upload_folder = 'static/images'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Generate a unique filename
        original_filename = secure_filename(file.filename.rsplit('.', 1)[0])  # Remove extension
        unique_suffix = str(int(time.time()))  # Use current timestamp as a unique identifier
        new_filename = f"{original_filename}_{unique_suffix}.{file_extension}"
        file_path = os.path.join(upload_folder, new_filename)
        file.save(file_path)

        # Save relative path (remove "static/" cause we are using the url_for() function)
        relative_path = f'images/{new_filename}'

        try:
            # Insert data into the database
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO packages (country, duration, person, price, description, image)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (destination, duration, person, price, description, relative_path))
            mysql.connection.commit()
            cur.close()

            flash(f'Package for "{destination}" added successfully!', 'success')
            return redirect(url_for('view_packages'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_packages'))

    return render_template('admin/add_packages.html')

@app.route('/admin/packages/delete/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Retrieve the package from the database to get the image path
        cur = mysql.connection.cursor()
        query = "SELECT image FROM packages WHERE id = %s"
        cur.execute(query, (package_id,))
        package = cur.fetchone()
        cur.close()

        if not package:
            flash('Package not found!', 'danger')
            return redirect(url_for('add_packages'))

        # Delete the image file if it exists
        image_path = os.path.join('static', package[0])  # Add 'static/' back to the relative path
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete the package from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM packages WHERE id = %s"
        cur.execute(query, (package_id,))
        mysql.connection.commit()
        cur.close()

        flash('Package deleted successfully!', 'success')
        return redirect(url_for('view_packages'))

    except Exception as e:
        flash(f"Error deleting package: {str(e)}", 'danger')
        return redirect(url_for('add_packages'))
    
@app.route('/admin/hotels')
def view_hotels():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `hotels`")
    hotels = cur.fetchall()
    cur.close()
    return render_template('admin/hotels.html', hotels=hotels)

@app.route('/admin/hotels/add', methods=['GET', 'POST'])
def add_hotel():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Fetch form data
        name = request.form.get('name')
        location = request.form.get('location')
        rating = request.form.get('rating')
        room_types = request.form.get('room_types')
        price_per_night = request.form.get('price_per_night')
        description = request.form.get('description')
        file = request.files.get('uploadfile')

        # Validate inputs
        if not name or not location or not rating or not room_types or not price_per_night or not description or not file:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_hotel'))

        # Allowed extensions
        allowed_extensions = {'jpg', 'bmp', 'webp', 'jpeg', 'png'}
        file_extension = file.filename.rsplit('.', 1)[-1].lower()

        if '.' not in file.filename or file_extension not in allowed_extensions:
            flash('Invalid file type! Please upload an image (jpg, bmp, webp, jpeg, png).', 'danger')
            return redirect(url_for('add_hotel'))

        # Handle file upload
        upload_folder = 'static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        original_filename = secure_filename(file.filename.rsplit('.', 1)[0])
        unique_suffix = str(int(time.time()))
        new_filename = f"{original_filename}_{unique_suffix}.{file_extension}"
        file_path = os.path.join(upload_folder, new_filename)
        file.save(file_path)

        # Save relative path (remove "static/")
        relative_path = f'uploads/{new_filename}'

        try:
            # Insert data into the database
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO hotels (name, location, rating, room_types, price_per_night, description, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (name, location, rating, room_types, price_per_night, description, relative_path))
            mysql.connection.commit()
            cur.close()

            flash('Hotel added successfully!', 'success')
            return redirect(url_for('view_hotels'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_hotel'))

    return render_template('admin/add_hotel.html')

@app.route('/admin/hotels/edit/<int:hotel_id>', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hotels WHERE id = %s", (hotel_id,))
    hotel = cur.fetchone()
    cur.close()

    if not hotel:
        flash('Hotel not found!', 'danger')
        return redirect(url_for('view_hotels'))

    if request.method == 'POST':
        # Fetch form data
        name = request.form.get('name')
        location = request.form.get('location')
        rating = request.form.get('rating')
        room_types = request.form.get('room_types')
        price_per_night = request.form.get('price_per_night')
        description = request.form.get('description')
        file = request.files.get('uploadfile')

        # Validate inputs
        if not name or not location or not rating or not room_types or not price_per_night or not description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('edit_hotel', hotel_id=hotel_id))

        # Handle file upload (optional)
        if file and file.filename:
            allowed_extensions = {'jpg', 'bmp', 'webp', 'jpeg', 'png'}
            file_extension = file.filename.rsplit('.', 1)[-1].lower()

            if '.' not in file.filename or file_extension not in allowed_extensions:
                flash('Invalid file type! Please upload an image (jpg, bmp, webp, jpeg, png).', 'danger')
                return redirect(url_for('edit_hotel', hotel_id=hotel_id))

            # Delete old image
            old_image_path = os.path.join('static', hotel[6])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            # Save new image
            upload_folder = 'static/uploads'
            original_filename = secure_filename(file.filename.rsplit('.', 1)[0])
            unique_suffix = str(int(time.time()))
            new_filename = f"{original_filename}_{unique_suffix}.{file_extension}"
            file_path = os.path.join(upload_folder, new_filename)
            file.save(file_path)

            relative_path = f'uploads/{new_filename}'
        else:
            relative_path = hotel[6]  # Keep the existing image path

        try:
            # Update hotel in the database
            cur = mysql.connection.cursor()
            query = """
                UPDATE hotels
                SET name = %s, location = %s, rating = %s, room_types = %s, price_per_night = %s, description = %s, image = %s
                WHERE id = %s
            """
            cur.execute(query, (name, location, rating, room_types, price_per_night, description, relative_path, hotel_id))
            mysql.connection.commit()
            cur.close()

            flash('Hotel updated successfully!', 'success')
            return redirect(url_for('view_hotels'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('edit_hotel', hotel_id=hotel_id))

    return render_template('admin/edit_hotel.html', hotel=hotel)

@app.route('/admin/hotels/delete/<int:hotel_id>', methods=['POST'])
def delete_hotel(hotel_id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT image FROM hotels WHERE id = %s", (hotel_id,))
    hotel = cur.fetchone()
    cur.close()

    if not hotel:
        flash('Hotel not found!', 'danger')
        return redirect(url_for('view_hotels'))

    # Delete image file
    image_path = os.path.join('static', hotel[0])  # Add 'static/' to relative path
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete hotel record
    try:
        cur = mysql.connection.cursor()
        query = "DELETE FROM hotels WHERE id = %s"
        cur.execute(query, (hotel_id,))
        mysql.connection.commit()
        cur.close()

        flash('Hotel deleted successfully!', 'success')
        return redirect(url_for('view_hotels'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('view_hotels'))

# View all tickets
@app.route('/admin/tickets')
def view_tickets():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `airline_tickets`")
    tickets = cur.fetchall()
    cur.close()
    return render_template('admin/view_tickets.html', tickets=tickets)

# View all flights
@app.route('/admin/flights')
def view_flights():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Fetch flight bookings
    cur.execute("""
        SELECT 
            f.id as id,
            f.email as email,
            f.ticket_type as ticket_type,
            f.departure_city as departure_city,
            f.destination_city as destination_city,
            f.departure_date as departure_date,
            f.return_date as return_date,
            f.flight_class as flight_class,
            f.status as status,
            GROUP_CONCAT(fp.name) as people 
        FROM `flights` f
        JOIN `flight_passengers` fp ON fp.flight_id = f.id
        GROUP BY f.id
        ORDER BY f.created_at DESC
    """)
    flights = cur.fetchall()
    cur.close()
    
    return render_template('admin/view_flights.html', flights=flights)

@app.route('/admin/flights/<int:id>')
def view_flight_details(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch flight bookings
    cur.execute("SELECT * FROM flights WHERE id = %s", (id,))
    flight = cur.fetchone()

    if not flight:
        flash('Flight not found!', 'danger')
        return redirect(url_for('view_flights'))
    
    # Fetch flight passengers
    cur.execute("SELECT * FROM flight_passengers WHERE flight_id = %s", (flight.get('id'),))
    passengers = cur.fetchall()

    print(passengers)

    cur.close()
    
    return render_template('admin/review_flight.html', flight=flight, passengers=passengers)

@app.route('/admin/accept-flight/<int:id>', methods=['GET'])
def flight_payment(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM flights WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Flight not found!', 'danger')
            return redirect(url_for('bookings'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE flights SET status='USER_PAYMENT' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Flight successfully accepted and awaiting payment.', 'success')
        return redirect(url_for('view_flights'))

    except Exception as e:
        flash(f'Error accepting flight: {str(e)}', 'danger')
        return redirect(url_for('view_flights'))
    
@app.route('/admin/paid-flight/<int:id>', methods=['GET'])
def flight_paid(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM flights WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Flight not found!', 'danger')
            return redirect(url_for('view_flights'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE flights SET status='PAID' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Flight successfully marked as PAID.', 'success')
        return redirect(url_for('view_flights'))

    except Exception as e:
        flash(f'Error marking flight as paid: {str(e)}', 'danger')
        return redirect(url_for('view_flights'))
    
@app.route('/admin/tickted-flight/<int:id>', methods=['GET'])
def flight_ticketed(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking details
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM flights WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Flight not found!', 'danger')
            return redirect(url_for('view_flights'))

        # Delete the booking from the bookings table
        cur.execute("UPDATE custom_tours SET status='TICKET' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Flight successfully marked as PAID and ticket generated.', 'success')
        return redirect(url_for('view_flights'))

    except Exception as e:
        flash(f'Error generating ticket for flight: {str(e)}', 'danger')
        return redirect(url_for('view_flights'))

@app.route('/admin/tickets/add', methods=['GET', 'POST'])
def add_ticket():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Fetch form data
        airline_name = request.form.get('airline_name')
        departure_location = request.form.get('departure_location')
        destination_location = request.form.get('destination_location')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        ticket_price = request.form.get('ticket_price')
        ticket_class = request.form.get('ticket_class')

        # Validate inputs
        if not airline_name or not departure_location or not destination_location or not departure_date or not ticket_price or not ticket_class:
            flash('All fields except Return Date are required!', 'danger')
            return redirect(url_for('add_ticket'))

        try:
            # Insert data into the database
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO airline_tickets (airline_name, departure_location, destination_location, departure_date, return_date, ticket_price, ticket_class)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (airline_name, departure_location, destination_location, departure_date, return_date, ticket_price, ticket_class))
            mysql.connection.commit()
            cur.close()

            flash('Airline Ticket added successfully!', 'success')
            return redirect(url_for('view_tickets'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_ticket'))

    return render_template('admin/add_ticket.html')

@app.route('/admin/tickets/edit/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM airline_tickets WHERE id = %s", (ticket_id,))
    ticket = cur.fetchone()
    cur.close()

    if not ticket:
        flash('Airline Ticket not found!', 'danger')
        return redirect(url_for('view_tickets'))

    if request.method == 'POST':
        # Fetch form data
        airline_name = request.form.get('airline_name')
        departure_location = request.form.get('departure_location')
        destination_location = request.form.get('destination_location')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        ticket_price = request.form.get('ticket_price')
        ticket_class = request.form.get('ticket_class')

        # Validate inputs
        if not airline_name or not departure_location or not destination_location or not departure_date or not ticket_price or not ticket_class:
            flash('All fields except Return Date are required!', 'danger')
            return redirect(url_for('edit_ticket', ticket_id=ticket_id))

        try:
            # Update ticket in the database
            cur = mysql.connection.cursor()
            query = """
                UPDATE airline_tickets
                SET airline_name = %s, departure_location = %s, destination_location = %s,
                    departure_date = %s, return_date = %s, ticket_price = %s, ticket_class = %s
                WHERE id = %s
            """
            cur.execute(query, (airline_name, departure_location, destination_location, departure_date, return_date, ticket_price, ticket_class, ticket_id))
            mysql.connection.commit()
            cur.close()

            flash('Airline Ticket updated successfully!', 'success')
            return redirect(url_for('view_tickets'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('edit_ticket', ticket_id=ticket_id))

    return render_template('admin/edit_ticket.html', ticket=ticket)

@app.route('/admin/tickets/delete/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM airline_tickets WHERE id = %s", (ticket_id,))
    ticket = cur.fetchone()
    cur.close()

    if not ticket:
        flash('Airline Ticket not found!', 'danger')
        return redirect(url_for('view_tickets'))

    try:
        # Delete ticket from the database
        cur = mysql.connection.cursor()
        query = "DELETE FROM airline_tickets WHERE id = %s"
        cur.execute(query, (ticket_id,))
        mysql.connection.commit()
        cur.close()

        flash('Airline Ticket deleted successfully!', 'success')
        return redirect(url_for('view_tickets'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('view_tickets'))

@app.route('/admin/users')
def users():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `users`")
    users = cur.fetchall()
    cur.close()
    return render_template('admin/users.html', users=users)

@app.route('/admin/admins')
def admins():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `admins`")
    admins = cur.fetchall()
    cur.close()
    return render_template('admin/admins.html', admins=admins)

@app.route('/admin/admins/add', methods=['GET', 'POST'])
def add_admin():
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        userpassword = request.form['userpassword']

        # Check if username exists
        cur.execute("SELECT * FROM `admins` WHERE `username` = %s", (username,))
        admin_exists = cur.fetchone()
        if admin_exists:
            flash('Username already exists!', 'danger')
            return redirect(url_for('add_admin'))

        if not username or not userpassword:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_admin'))

        cur.execute("INSERT INTO `admins` (`id`, `username`, `userpassword`) VALUES (NULL, %s, %s)", (username, userpassword))
        mysql.connection.commit()
        cur.close()

        flash('Admin added successfully!', 'success')
        return redirect(url_for('admins'))
    return render_template('admin/add_admin.html')

@app.route('/admin/admins/edit/<int:id>', methods=['GET', 'POST'])
def edit_admin(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `admins` WHERE `id` = %s", (id,))
    admin = cur.fetchone()

    if not admin:
        flash('Admin not found!', 'danger')
        return redirect(url_for('admins'))

    if request.method == 'POST':
        username = request.form['username']
        userpassword = request.form['userpassword']

        # Check if username exists
        cur.execute("SELECT * FROM `admins` WHERE `username` = %s and `id` != %s", (username,id,))
        admin_exists = cur.fetchone()
        if admin_exists:
            flash('Username already exists!', 'danger')
            return redirect(url_for('edit_admin', id=id))

        if not username or not userpassword:
            flash('All fields are required!', 'danger')
            return redirect(url_for('edit_admin', id=id))
        
        cur.execute("UPDATE admins SET `username` = %s, `userpassword` = %s WHERE `id` = %s", (username, userpassword, id))
        mysql.connection.commit()
        cur.close()
        
        flash('Admin updated successfully!', 'success')
        return redirect(url_for('admins'))

    return render_template('admin/edit_admin.html', admin=admin)

@app.route('/admin/admins/delete/<int:id>', methods=['GET'])
def delete_admin(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `admins` WHERE `id` = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('admins'))

# Public routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the form was submitted
    if request.method == 'POST':
        # Replace with your actual validation logic
        input_username = request.form['username']
        input_password = request.form['userpass']
        input_usertype = request.form['usertype']

        if not input_usertype:
            flash('Username already exists!', 'danger')
            return redirect(url_for('login'))
        # Selection of the table from the user is going to be authenticted from
        # The user trying to login can be admin or a normal user
        db_table = 'admins' if input_usertype == 'admin' else 'users'
        # Which field to check the username with (depends on the different tables in the database)
        username_field = 'username' if input_usertype == 'admin' else 'name'
        # Which field to check the password with (depends on the different tables in the database)
        password_field_index = 2 if input_usertype == 'admin' else 3
        # Search the user
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {db_table} WHERE `{username_field}` = %s", (input_username,))
        existing_user = cur.fetchone()
        # Checks if the user was found
        if existing_user:
            # Ensure only one session per device
            if session.get('user'):
                flash("You are already logged in on another tab.", "warning")
                return redirect(url_for('home'))
            # Now check if the password matches the user
            if existing_user[ password_field_index ] == input_password:
                session['user'] = existing_user
                session['username'] = input_username
                session['usertype'] = input_usertype
                # Inject JavaScript after successful login to set localStorage
                response = make_response(redirect(url_for('home')))
                response.set_cookie('user_logged_in', 'true')
                return response
            # If the passwords do not match
            flash('Incorrect username or password', 'danger')
            return redirect(url_for('login'))
        # If the user was not found
        flash('Username not found', 'danger')
        return redirect(url_for('login'))
    # If the form was not submitted
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # If the form was submitted
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate inputs
        if not name or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        try:
            # Insert into database
            cur = mysql.connection.cursor()
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cur.execute(query, (name, email, password))
            mysql.connection.commit()
            cur.close()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('register'))
    # If the form was not submitted
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Loop through all the values of the session and unset them
    for session_name in ['user', 'username', 'usertype']:
        session.pop(session_name, None) # Unset the value of the session

    session.clear()
    # Redirects to login page
    flash('User logged out successfully!', 'success')
    response = make_response(redirect(url_for('login')))
    response.set_cookie('user_logged_in', '', expires=0)  # Clears the cookie
    return response
    #return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html', logged_in=logged_in())

@app.route('/custom-tour', methods=['GET', 'POST'])
def custom_tour():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `packages` ORDER BY `id` DESC")
    packages = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        num_travelers = int(request.form.get('num-travelers', 1))
        countries = request.form.getlist('countries[]')
        #hotel_type = request.form.get('hotel-type')
        #flight_class = request.form.get('flight-class')
        details = request.form.get('details')

        # Validate data
        if not name or not email or not address or not countries:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('custom_tour'))

        travelers = []
        for i in range(1, num_travelers + 1):
            traveler = {
                'name': request.form.get(f'traveler_{i}_name'),
                'email': request.form.get(f'traveler_{i}_email'),
                'phone': request.form.get(f'traveler_{i}_phone'),
                'hotel_type': request.form.get(f'traveler_{i}_hotel_type'),
                'flight_class': request.form.get(f'traveler_{i}_flight_class'),
            }
            travelers.append(traveler)

        destinations = []
        for country in countries:
            start_date = request.form.get(f'start_dates[{country}]')
            end_date = request.form.get(f'end_dates[{country}]')
            
            # Ensure start date and end date are valid
            if start_date and end_date:
                if datetime.strptime(start_date, '%Y-%m-%d') >= datetime.strptime(end_date, '%Y-%m-%d'):
                    flash(f'End date must be after start date for {country}.', 'danger')
                    return redirect(url_for('custom_tour'))
            
            destinations.append({'country': country, 'start_date': start_date, 'end_date': end_date})
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `custom_tours` (name, email, address, details) VALUES (%s, %s, %s, %s)", (name, email, address, details))
        tour_id = cur.lastrowid

        for traveler in travelers:
            cur.execute("INSERT INTO `tour_travelers` (tour_id, name, email, phone, hotel_type, flight_class) VALUES (%s, %s, %s, %s, %s, %s)",
                        (tour_id, traveler['name'], traveler['email'], traveler['phone'], traveler['hotel_type'], traveler['flight_class']))

        for destination in destinations:
            cur.execute("INSERT INTO `tour_destinations` (tour_id, country, start_date, end_date) VALUES (%s, %s, %s, %s)",
                        (tour_id, destination['country'], destination['start_date'], destination['end_date']))

        mysql.connection.commit()
        cur.close()
        flash('Your itinerary has been submitted successfully!', 'success')
        #return redirect(url_for('custom_tour'))
        # Return success response
        return jsonify({'success': True, 'message': 'Your itinerary has been submitted successfully'})
    
    return render_template('custom-tour.html', logged_in=logged_in(), packages=packages)

@app.route('/hotels')
def hotels():
    return render_template('hotels.html', logged_in=logged_in())

@app.route('/flights', methods=['GET', 'POST'])
def flights():  
    if request.method == 'POST':
        booker_email = request.form.get('booker_email')
        ticket_type = request.form.get('ticket_type')
        departure_city = request.form.get('departure_city')
        destination_city = request.form.get('destination_location')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date') if ticket_type == 'return' else None
        passengers = int(request.form.get('passengers', 1))
        flight_class = request.form.get('flight_class')

        # Validate that departure date is not in the past
        today = datetime.today().strftime('%Y-%m-%d')
        if departure_date < today:
            flash('Departure date cannot be in the past.', 'danger')
            return redirect(url_for('flights'))
        if return_date and return_date < departure_date:
            flash('Return date must be after the departure date.', 'danger')
            return redirect(url_for('flights'))

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO `flights` (email, ticket_type, departure_city, destination_city, departure_date, return_date, flight_class)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (booker_email, ticket_type, departure_city, destination_city, departure_date, return_date, flight_class))
        flight_id = cur.lastrowid

        for i in range(1, passengers + 1):
            passenger_name = request.form.get(f'passenger_{i}_name')
            passenger_contact = request.form.get(f'passenger_{i}_contact')
            passenger_email = request.form.get(f'passenger_{i}_email')
            passport_number = request.form.get(f'passenger_{i}_passport')
            passport_country = request.form.get(f'passenger_{i}_passport_country')
            passport_issue = request.form.get(f'passenger_{i}_passport_issue')
            passport_picture = request.files.get(f'passenger_{i}_passport_picture')

            # Allowed extensions
            allowed_extensions = {'jpg', 'bmp', 'webp', 'jpeg', 'png'}
            if passport_picture:
                file_extension = passport_picture.filename.rsplit('.', 1)[-1].lower()
                if file_extension not in allowed_extensions:
                    return jsonify({"success": False, "message": "Invalid file type! Please upload an image (jpg, bmp, webp, jpeg, png)."}), 400

                # Handle file upload
                upload_folder = 'static/images'
                os.makedirs(upload_folder, exist_ok=True)

                # Generate a unique filename
                original_filename = secure_filename(passport_picture.filename.rsplit('.', 1)[0])
                unique_suffix = str(int(time.time()))  # Use current timestamp as a unique identifier
                new_filename = f"{original_filename}_{unique_suffix}.{file_extension}"
                file_path = os.path.join(upload_folder, new_filename)
                passport_picture.save(file_path)

                # Save relative path (for URL referencing)
                relative_path = f'images/{new_filename}'
            else:
                relative_path = None

            cur.execute("""
                INSERT INTO `flight_passengers` (flight_id, name, contact, email, passport_number, passport_country, passport_issue, passport_picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (flight_id, passenger_name, passenger_contact, passenger_email, passport_number, passport_country, passport_issue, relative_path))

        mysql.connection.commit()
        cur.close()

        flash('Flight booking submitted successfully!', 'success')
        return redirect(url_for('flights'))
        # Return success response
        return jsonify({'success': True, 'message': 'Your booking submitted successfully'})
    
    return render_template('flights.html', logged_in=logged_in())

@app.route('/packages')
def packages_front():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `packages` ORDER BY `id` DESC")
    packages = cur.fetchall()
    cur.close()
    return render_template('packages.html', logged_in=logged_in(), packages=packages)

@app.route('/packages/<int:id>', methods=['GET', 'POST'])
def view_package(id):
    #cur = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `packages` WHERE `id` = %s", (id,))
    package = cur.fetchone()

    print(package['country'])

    if not package:
        flash('Package not found!', 'danger')
        return redirect(url_for('packages_front'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        num_travelers = int(request.form.get('num-travelers', 1))
        country = request.form.get('country')
        hotel_type = request.form.get('hotel_type')
        flight_class = request.form.get('flight_class')
        details = request.form.get('details')

        # Validate data
        if not name or not email or not address or not country:
            return jsonify({'success': False, 'message': 'Please fill in all required fields'})

        travelers = []
        for i in range(1, num_travelers + 1):
            traveler = {
                'name': request.form.get(f'traveler_{i}_name'),
                'email': request.form.get(f'traveler_{i}_email'),
                'phone': request.form.get(f'traveler_{i}_phone'),
                'hotel_type': hotel_type,
                'flight_class': flight_class,
            }
            travelers.append(traveler)

        destinations = []
        
        start_date = request.form.get(f'start_date')
        end_date = request.form.get(f'end_date')
        
        # Ensure start date and end date are valid
        if start_date and end_date:
            if datetime.strptime(start_date, '%Y-%m-%d') >= datetime.strptime(end_date, '%Y-%m-%d'):
                #flash(f'End date must be after start date for {country}.', 'danger')
                #return redirect(url_for('custom_tour'))
                return jsonify({'success': False, 'message': f'End date must be after start date for {country}.'})
        
        
        cur.execute("INSERT INTO `bookings` (byuser, name, email, country, travel_date, members, days, price, hotel_type, flight_class, special_request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (str(name).lower(), name, email, package['country'], start_date, package['person'], package['duration'], package['price'], hotel_type, flight_class, details))
        booking_id = cur.lastrowid

        for traveler in travelers:
            cur.execute("INSERT INTO `booking_travelers` (booking_id, name, email, phone, hotel_type, flight_class) VALUES (%s, %s, %s, %s, %s, %s)",
                        (booking_id, traveler['name'], traveler['email'], traveler['phone'], hotel_type, flight_class))

        mysql.connection.commit()
        cur.close()
        flash('Your itinerary has been submitted successfully!', 'success')
        #return redirect(url_for('custom_tour'))
        # Return success response
        return jsonify({'success': True, 'message': 'Your itinerary has been submitted successfully'})
        
    return render_template('package-info.html', logged_in=logged_in(), package=package)

@app.route('/my-bookings')
def my_bookings():
    # Checks if the user is logged in
    if not logged_in():
        flash("Please login first!", "danger")
        return redirect(url_for('login'))
    
    if is_admin():
        return redirect(url_for('dashboard'))
    
    # Get the user's email from the session
    user_email = session['user'][2]

    # Fetch pending bookings
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bookings WHERE email = %s and approved=0", (user_email,))
    bookings_pending = cur.fetchall()

    # Fetch approved bookings (tickets)
    cur.execute("SELECT * FROM bookings WHERE email = %s and approved=1", (user_email,))
    bookings_approved = cur.fetchall()

    # Fetch cancelled bookings (tickets)
    cur.execute("SELECT * FROM cancelled_bookings WHERE email = %s", (user_email,))
    bookings_cancelled = cur.fetchall()

    # Fetch custom tours
    cur.execute("""
        SELECT 
            GROUP_CONCAT(td.country) as country, 
            GROUP_CONCAT(tt.name) as people, 
            ct.id as id,
            ct.name as name,
            ct.email as email,
            ct.address as address,
            ct.details as details,
            ct.status as status,
            COUNT(DISTINCT td.id) AS total_tours, 
            COUNT(DISTINCT tt.id) AS total_people 
        FROM `custom_tours` ct
        JOIN `tour_destinations` td ON td.tour_id = ct.id
        LEFT JOIN `tour_travelers` tt ON tt.tour_id = ct.id
        WHERE ct.email = %s
        GROUP BY ct.id
    """, (user_email,))
    custom_tours = cur.fetchall()

    # Fetch flight bookings
    cur.execute("""
        SELECT 
            f.id as id,
            f.email as email,
            f.ticket_type as ticket_type,
            f.departure_city as departure_city,
            f.destination_city as destination_city,
            f.departure_date as departure_date,
            f.return_date as return_date,
            f.flight_class as flight_class,
            f.status as status,
            GROUP_CONCAT(fp.name) as people 
        FROM `flights` f
        JOIN `flight_passengers` fp ON fp.flight_id = f.id
        WHERE f.email = %s
        GROUP BY f.id
        ORDER BY f.created_at DESC
    """, (user_email,))
    flights = cur.fetchall()

    cur.close()

    return render_template('my-bookings.html', logged_in=logged_in(), 
                                bookings_pending=bookings_pending, 
                                bookings_approved=bookings_approved, 
                                bookings_cancelled=bookings_cancelled,
                                custom_tours=custom_tours,
                                flights=flights
                           )

@app.route('/add-booking', methods=['POST'])
def add_booking():
    if request.method == 'POST':
        if not logged_in():
            flash("Login required!", "danger")
            return redirect(url_for('login'))
        
        try:
            # Extract and process form data
            name = request.form.get('name')
            email = request.form.get('email')
            country = request.form.get('country')
            date = request.form.get('date')
            members = request.form.get('members')
            number_of_days = request.form.get('number-of-days')
            hotel_type = request.form.get('hotel-type')
            flight_class = request.form.get('flight-class')
            message = request.form.get('message')
            
            byuser = session.get('username')

            # Validate fields
            if not (name and email and country and date and members and number_of_days and hotel_type and flight_class):
                return jsonify({'success': False, 'message': 'All fields except Special Request are required.'})

            # Insert into the database
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO bookings (byuser, name, email, country, travel_date, members, days, hotel_type, flight_class, special_request)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (byuser, name, email, country, date, members, number_of_days, hotel_type, flight_class, message))
            mysql.connection.commit()
            cur.close()

            # Return success response
            return jsonify({'success': True, 'message': 'Booking successfully created!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/add-defined-booking', methods=['POST'])
def add_defined_booking():
    if request.method == 'POST':
        if not logged_in():
            flash("Login required!", "danger")
            return redirect(url_for('login'))
        
        try:
            # Extract and process form data
            name = request.form.get('name')
            email = request.form.get('email')
            country = request.form.get('country')
            date = request.form.get('date')
            members = request.form.get('members')
            number_of_days = request.form.get('number-of-days')
            hotel_type = request.form.get('hotel-type')
            flight_class = request.form.get('flight-class')
            message = request.form.get('message')
            
            byuser = session.get('username')

            # Validate fields
            if not (name and email and country and date and members and number_of_days and hotel_type and flight_class):
                return jsonify({'success': False, 'message': 'All fields except Special Request are required.'})

            # Insert into the database
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO bookings (byuser, name, email, country, travel_date, members, days, hotel_type, flight_class, special_request)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (byuser, name, email, country, date, members, number_of_days, hotel_type, flight_class, message))
            mysql.connection.commit()
            cur.close()

            # Return success response
            return jsonify({'success': True, 'message': 'Booking successfully created!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/cancel-booking/<int:id>', methods=['POST'])
def cancel_booking(id):
    # Checks for authentication
    if not logged_in() or not is_admin():
        flash("Login required", 'danger')
        return redirect(url_for('login'))
    
    try:
        # Fetch the booking to ensure it exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        booking = cur.fetchone()

        if not booking:
            flash('Booking not found!', 'danger')
            return redirect(url_for('my_bookings'))

        # Delete the booking
        cur.execute("DELETE FROM bookings WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash('Booking successfully canceled.', 'success')
        return redirect(url_for('my_bookings'))

    except Exception as e:
        flash(f'Error canceling booking: {str(e)}', 'danger')
        return redirect(url_for('my_bookings'))

@app.template_filter('currency')
def currency_format(value):
    try:
        return "Rs.{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return "£0.00"
    
@app.template_filter('status')
def status_format(value):
    try:
        v = str(value).lower()
        if v == 'pending':
            return 'Pending Admin Approval'
        elif v == 'confirmed':
            return 'Admin Confirmed'
        elif v == 'cancelled':
            return 'Cancelled'
        elif v == 'rejected':
            return 'Admin Rejected'
        elif v == 'user_payment':
            return 'Awaiting User Payment'
        elif v == 'paid':
            return 'Payment Received'
        elif v == 'ticket':
            return 'Ticket Uploaded'
        else:
            return 'Unknown'
        
    except (ValueError, TypeError):
        return "Unknown"

def logged_in():
    return 'username' in session

def is_admin():
    return 'usertype' in session and session['usertype'] == 'admin'

if __name__ == '__main__':
    app.run(debug=True)
