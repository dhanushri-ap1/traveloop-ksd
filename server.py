from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from geopy.geocoders import Nominatim
import uuid

app = Flask(__name__, template_folder='static')
app.secret_key = 'your_secret_key'

# Initialize Geocoder
geolocator = Nominatim(user_agent="traveloop_explorer")

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shas@8131mi'
app.config['MYSQL_DB'] = 'traveloop'
# Use DictCursor to make returning JSON data much easier
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# --- EXISTING ROUTES (UNTOUCHED) ---

@app.route('/')
def home():
    return render_template('auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST': 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = str(uuid.uuid4())

        cur = mysql.connection.cursor()
        try: 
            cur.execute("INSERT INTO users(id, first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s, %s)", 
                        (user_id, first_name, last_name, email, pw_hash))
            mysql.connection.commit()
            flash('Account created! Please login.', 'success')
        except Exception as e: 
            flash('This email is already registered. Please use a different one.', 'danger')
        finally:
            cur.close()
        return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password_candidate = request.form['password']

    cur = mysql.connection.cursor()
    # Note: With DictCursor, we fetch differently
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cur.fetchone()

    if user:
        if bcrypt.check_password_hash(user['password_hash'], password_candidate):
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['name'] = user['first_name']
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
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('home'))

@app.route('/chatbot')
def chatbot():
    if 'logged_in' in session: 
        return render_template('pr.html', name=session['name'])
    return redirect(url_for('home'))

@app.route('/todo')
def todo():
    if 'logged_in' in session: 
        return render_template('todolist.html')
    return redirect(url_for('home'))

@app.route('/scrap')
def scrap(): 
    if 'logged_in' in session: 
        return render_template('scrapbook.html', name=session['name'])
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'logged_in' in session: 
        return render_template('profile.html', name=session['name'])
    return redirect(url_for('home'))

# --- NEW API ROUTES FOR PROFILE FUNCTIONALITY ---

@app.route('/api/get_profile_data', methods=['GET'])
def get_profile_data():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Fetch user's countries
    cur.execute("SELECT flag, country, city, year, status FROM user_countries WHERE user_id = %s", [user_id])
    countries = cur.fetchall()
    
    # Fetch user's places (stamps)
    cur.execute("SELECT icon, name, country_str as country, visit_date as date, status FROM user_places WHERE user_id = %s", [user_id])
    places = cur.fetchall()
    
    cur.close()
    return jsonify({
        "name": session['name'],
        "countries": countries,
        "places": places
    })

@app.route('/api/add_country', methods=['POST'])
def add_country():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO user_countries (id, user_id, flag, country, city, year, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), session['user_id'], data['flag'], data['country'], data['city'], data['year'], data['status']))
        mysql.connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

@app.route('/api/add_place', methods=['POST'])
def add_place():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO user_places (id, user_id, icon, name, country_str, visit_date, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), session['user_id'], data['icon'], data['name'], data['country'], data['date'], data['status']))
        mysql.connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(debug=True)