# ZHS Travel & Tours - Online Booking System

![Travel & Tours](https://img.shields.io/badge/Travel-Tours-blue.svg) ![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg) ![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-purple.svg)

A comprehensive web-based travel and tours booking management system built with Flask and MySQL. This system allows customers to book tour packages, flights, hotels, and custom tours while providing administrators with a powerful dashboard to manage all bookings and services.

## 📸 Screenshots

### User Interface
- **Homepage**: Beautiful landing page showcasing featured tour packages
- **Package Booking**: Interactive forms for booking predefined tour packages
- **Custom Tours**: Create personalized itineraries with multiple destinations
- **Flight Booking**: Book domestic and international flights with passenger details
- **Hotel Reservations**: Browse and book hotels by location
- **My Bookings**: Track all bookings with status updates

### Admin Dashboard
- **Analytics Dashboard**: Overview of bookings, users, and revenue
- **Booking Management**: Approve/reject bookings and manage payment status
- **Package Management**: Add, edit, and delete tour packages
- **Hotel Management**: Manage hotel listings and details
- **Flight Management**: Review and process flight booking requests
- **User Management**: Manage registered users and administrators

## 🚀 Features

### For Customers
- **User Registration & Authentication**: Secure user accounts with session management
- **Tour Package Booking**: Browse and book predefined tour packages
- **Custom Tour Planning**: Create personalized multi-destination itineraries
- **Flight Reservations**: Book one-way or round-trip flights with passenger details
- **Hotel Bookings**: Search and book hotels by country and city
- **Booking Management**: View, track, and cancel bookings
- **Payment Integration**: Secure payment processing for confirmed bookings
- **Responsive Design**: Mobile-friendly interface for all devices

### For Administrators
- **Comprehensive Dashboard**: Real-time analytics and booking statistics
- **Booking Workflow Management**: 
  - Approve/reject customer bookings
  - Manage payment status (Pending → User Payment → Paid → Ticketed)
  - Handle cancellations and refunds
- **Content Management**:
  - Add/edit/delete tour packages with images
  - Manage hotel listings and details
  - Create and manage airline tickets
- **User Management**: Manage customer accounts and admin users
- **Flight Proposal System**: Review flight requests and propose options
- **Payment Tracking**: Monitor all transactions and payment statuses

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.0 (Python)
- **Database**: MySQL with Flask-MySQLdb
- **Authentication**: Session-based authentication
- **File Handling**: Werkzeug for secure file uploads
- **PDF Generation**: FPDF for ticket generation

### Frontend
- **UI Framework**: Bootstrap 5.0+
- **Icons**: Font Awesome 5.10.0 + Bootstrap Icons
- **Animations**: WOW.js, Animate.css
- **Components**: Owl Carousel, Waypoints
- **JavaScript**: jQuery 3.4.1, Custom form handling

### Development Tools
- **Environment**: Python 3.8+
- **Database Client**: MySQLdb/PyMySQL
- **Image Processing**: Secure file upload with validation
- **Responsive Design**: Mobile-first approach

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed
- **MySQL Server** running (XAMPP, WAMP, or standalone)
- **pip** package manager
- **Git** (for cloning the repository)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sheikhamir/zhs.git
cd "zha Travel & Tours"
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. **Start MySQL Server** (using XAMPP/WAMP or standalone MySQL)

2. **Create Database**:
   ```sql
   CREATE DATABASE zhs;
   ```

3. **Import Database Schema**:
   ```bash
   mysql -u root -p zhs < zhs.sql
   ```

4. **Configure Database Connection** in `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
   app.config['MYSQL_DB'] = 'zhs'
   ```

### 5. Create Required Directories
```bash
mkdir -p static/images
mkdir -p static/uploads
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 🗃️ Database Structure

The system uses the following main tables:

### Core Tables
- **`users`**: Customer account information
- **`admins`**: Administrator accounts
- **`packages`**: Tour package details with pricing
- **`hotels`**: Hotel listings with location and amenities
- **`airline_tickets`**: Available flight options

### Booking Tables
- **`bookings`**: Tour package bookings with approval workflow
- **`custom_tours`**: Custom tour requests
- **`tour_destinations`**: Multi-destination tour details
- **`tour_travelers`**: Traveler information for custom tours
- **`flights`**: Flight booking requests
- **`flight_passengers`**: Passenger details for flight bookings
- **`cancelled_bookings`**: Record of cancelled bookings

### Payment & Processing
- **`payments`**: Payment transaction records
- **`flight_details`**: Proposed flight options from admin
- **`tickets`**: Generated tickets for approved bookings

## 🔐 Default Admin Credentials

```
Username: admin
Password: admin
```

**⚠️ Important**: Change the default admin credentials after first login!

## 🎯 Usage Guide

### For Customers

1. **Registration**: Create an account on the registration page
2. **Browse Packages**: Explore available tour packages on the homepage
3. **Book Tours**: 
   - Select a package and fill booking details
   - Or create a custom tour with multiple destinations
4. **Flight Booking**: Search and book flights with passenger information
5. **Hotel Booking**: Browse hotels by location and make reservations
6. **Track Bookings**: Monitor booking status in "My Bookings" section
7. **Payment**: Complete payment when booking is approved by admin

### For Administrators

1. **Login**: Access admin panel at `/admin`
2. **Dashboard**: Monitor key metrics and recent activities
3. **Manage Bookings**: 
   - Review and approve/reject customer bookings
   - Update payment status and upload tickets
4. **Content Management**:
   - Add new tour packages with descriptions and images
   - Manage hotel listings and flight options
5. **User Management**: View customer accounts and add new admins
6. **Flight Proposals**: Review flight requests and propose options with pricing

## 📁 Project Structure

```
zha Travel & Tours/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── zhs.sql                    # Database schema and sample data
├── static/                    # Static assets
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   ├── images/                # Uploaded package images
│   ├── uploads/               # Uploaded hotel images
│   └── lib/                   # Third-party libraries
├── templates/                 # HTML templates
│   ├── admin/                 # Admin panel templates
│   ├── payment/               # Payment processing templates
│   ├── *.html                 # Public page templates
│   └── template.*.html        # Base templates
├── images/                    # Static image assets
├── Video/                     # Demo videos
└── zhs/                       # Legacy/backup files
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production deployment:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=your-db-user
MYSQL_PASSWORD=your-db-password
MYSQL_DB=zhs
```

### File Upload Settings
- **Allowed Image Formats**: JPG, JPEG, PNG, BMP, WEBP
- **Upload Directories**: 
  - Package images: `static/images/`
  - Hotel images: `static/uploads/`
- **File Naming**: Automatic unique filename generation with timestamps

### Security Settings
- **Session Management**: Secure session handling with secret key
- **File Upload Security**: File type validation and secure filename generation
- **SQL Injection Protection**: Parameterized queries throughout the application

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   ```

2. **Configure Database** for production MySQL server

3. **Use WSGI Server** (Gunicorn recommended):
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 app:app
   ```

4. **Reverse Proxy** (Nginx configuration example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/your/app/static;
       }
   }
   ```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write descriptive commit messages
- Test all functionality before submitting PR
- Update documentation for new features

## 📝 API Endpoints

### Public Routes
- `GET /` - Homepage with featured packages
- `GET /packages` - Browse all tour packages
- `GET /packages/<id>` - View specific package details
- `GET /hotels` - Browse hotel listings
- `GET /flights` - Flight booking form
- `POST /custom-tour` - Submit custom tour request

### User Routes (Authentication Required)
- `GET /my-bookings` - View user's bookings
- `POST /add-booking` - Create new booking
- `GET /make-payment/<id>` - Payment processing

### Admin Routes (Admin Authentication Required)
- `GET /admin` - Admin dashboard
- `GET /admin/bookings` - Manage all bookings
- `GET /admin/packages` - Manage tour packages
- `GET /admin/hotels` - Manage hotel listings
- `GET /admin/flights` - Manage flight bookings
- `GET /admin/users` - User management

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify MySQL server is running
   - Check database credentials in `app.py`
   - Ensure database `zhs` exists

2. **File Upload Issues**:
   - Check directory permissions for `static/images/` and `static/uploads/`
   - Verify file size limits

3. **Session Issues**:
   - Clear browser cookies
   - Check secret key configuration

4. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate virtual environment

### Debug Mode
Enable debug mode for development:
```python
app.run(debug=True)
```

## 📞 Support

For support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/sheikhamir/zhs/issues)
- **Email**: [Contact maintainer](mailto:support@example.com)
- **Documentation**: Check inline code comments for detailed explanations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask Community** for the excellent web framework
- **Bootstrap Team** for the responsive UI components
- **Font Awesome** for the beautiful icons
- **MySQL** for reliable database management
- **Contributors** who have helped improve this project

---

**Made with ❤️ for the travel industry**

*Happy Travels! 🌍✈️🏨*
