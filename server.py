from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from geopy.geocoders import Nominatim  # Import Geocoder
import uuid

app = Flask(__name__, template_folder='static')
app.secret_key = 'your_secret_key'

# Initialize Geocoder (User_agent should be unique to your app)
geolocator = Nominatim(user_agent="traveloop_explorer")

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shas@8131mi'
app.config['MYSQL_DB'] = 'traveloop'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        # Get form data [cite: 31]
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = str(uuid.uuid4())

        cur = mysql.connection.cursor()
        try:
            # This will fail because of the UNIQUE KEY uq_users_email (email) in your schema
            cur.execute("INSERT INTO users(id, first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s, %s)", 
                        (user_id, first_name, last_name, email, pw_hash))
            mysql.connection.commit()
            flash('Account created! Please login.', 'success')
        except Exception as e:
            # This captures the MySQL duplicate entry error
            flash('This email is already registered. Please use a different one.', 'danger')
        finally:
            cur.close()
        return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password_candidate = request.form['password']

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

    if result > 0:
        data = cur.fetchone()
        # Your schema: email is index 3, password_hash is index 4 (0-indexed)
        password_hash = data[4]

        if bcrypt.check_password_hash(password_hash, password_candidate):
            session['logged_in'] = True
            session['user_id'] = data[0]
            session['name'] = data[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login', 'danger')
    else:
        flash('User not found', 'danger')
    
    cur.close()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        # Now Flask will look in 'static/dashboard.html'
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('home'))

@app.route('/chatbot')
def chatbot():
    if 'logged_in' in session:
        # Flask looks for static/mapping3.html based on your app config
        return render_template('pr.html')
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)