from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database Configuration (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///busgo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Route to redirect if unauthorized

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Bookings Model (updated)
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    fan = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables (run once)
with app.app_context():
    db.create_all()

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken!', 'error')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Create new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# Protect Booking Routes (Example)
@app.route('/book_now', methods=['POST'])
@login_required
def book_now():
    return redirect(url_for('route_selection'))

# Update Booking Confirmation to Show User-Specific Bookings
@app.route('/booking_confirmation')
@login_required
def booking_confirmation():
    latest_booking = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.id.desc()).first()
    if latest_booking:
        return render_template(
            'booking_confirmation.html',
            booking_id=latest_booking.id,
            departure=latest_booking.departure,
            destination=latest_booking.destination,
            payment_method=latest_booking.payment_method
        )
    flash('No booking found.', 'error')
    return redirect(url_for('home'))

# Rest of your existing routes (route_selection, passenger_identification, etc.)
# Ensure they use @login_required where needed.

if __name__ == '__main__':
    app.run(debug=True)