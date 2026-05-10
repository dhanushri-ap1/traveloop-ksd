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
app.config['MYSQL_PASSWORD'] = 'kesi@6549'
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

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# --- MEMORY / SCRAPBOOK API ROUTES ---

@app.route('/save_memory', methods=['POST'])
def save_memory():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401
    
    data = request.get_json()
    image_base64 = data.get('image') 
    description = data.get('description')
    user_id = session['user_id']

    # Remove metadata prefix (e.g., "data:image/jpeg;base64,") before saving to DB
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    cur = mysql.connection.cursor()
    # Inserting into the 'memories' table linked to the current user
    cur.execute("INSERT INTO memories (user_id, image_data, description) VALUES (%s, %s, %s)", 
                (user_id, image_base64, description))
    mysql.connection.commit()
    cur.close()
    return {"message": "Memory saved successfully!"}, 200

@app.route('/get_memories')
def get_memories():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401
    
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    # Fetch image data from your MySQL 'memories' table
    cur.execute("SELECT id, image_data, description FROM memories WHERE user_id = %s ORDER BY created_at DESC", [user_id])
    rows = cur.fetchall()
    cur.close()

    memories = []
    for row in rows:
        memories.append({
            "id": row[0],
            # CRITICAL FIX: The f-string adds the prefix the browser needs to render the image
            "image": f"data:image/jpeg;base64,{row[1]}", 
            "description": row[2]
        })
    return {"memories": memories}

@app.route('/delete_memory/<int:id>', methods=['DELETE'])
def delete_memory(id):
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401
    
    cur = mysql.connection.cursor()
    # Ensure the user can only delete their own images
    cur.execute("DELETE FROM memories WHERE id = %s AND user_id = %s", (id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return {"message": "Memory deleted"}, 200

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))

# --- TRIPS API ---

@app.route('/api/trips', methods=['GET', 'POST'])
def handle_trips():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cur = mysql.connection.cursor()
    uid = session['user_id']

    if request.method == 'POST':
        data = request.json
        cur.execute(
            'INSERT INTO trips (user_id, name, destination, budget, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)',
            (uid, data['name'], data.get('dest'), data.get('budget') or None,
             data.get('start') or None, data.get('end') or None)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"status": "success"})

    cur.execute('SELECT * FROM trips WHERE user_id = %s ORDER BY created_at DESC', (uid,))
    trips = cur.fetchall()
    cur.close()
    return jsonify(trips)

@app.route('/api/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM trips WHERE id = %s AND user_id = %s', (trip_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"status": "deleted"})

# --- WISHLIST API ---

@app.route('/api/wishlist', methods=['GET', 'POST'])
def handle_wishlist():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cur = mysql.connection.cursor()
    uid = session['user_id']

    if request.method == 'POST':
        data = request.json
        cur.execute('INSERT INTO wishlist_items (user_id, item_name) VALUES (%s, %s)', (uid, data['name']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"status": "success"})

    cur.execute('SELECT * FROM wishlist_items WHERE user_id = %s', (uid,))
    items = cur.fetchall()
    cur.close()
    return jsonify(items)

@app.route('/api/wishlist/<int:item_id>', methods=['DELETE', 'PATCH'])
def update_wishlist_item(item_id):
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cur = mysql.connection.cursor()
    uid = session['user_id']

    if request.method == 'DELETE':
        cur.execute('DELETE FROM wishlist_items WHERE id = %s AND user_id = %s', (item_id, uid))
        mysql.connection.commit()
        cur.close()
        return jsonify({"status": "deleted"})

    # PATCH — toggle is_completed
    data = request.json
    cur.execute(
        'UPDATE wishlist_items SET is_completed = %s WHERE id = %s AND user_id = %s',
        (1 if data.get('completed') else 0, item_id, uid)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"status": "updated"})

# --- STATS API ---

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if 'logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    cur = mysql.connection.cursor()
    uid = session['user_id']

    cur.execute('SELECT COUNT(*) as total_trips, SUM(budget) as total_budget FROM trips WHERE user_id = %s', (uid,))
    trip_stats = cur.fetchone()

    cur.execute('SELECT COUNT(*) as wishlist_count FROM wishlist_items WHERE user_id = %s', (uid,))
    wish_stats = cur.fetchone()

    cur.close()
    return jsonify({
        "trips": trip_stats['total_trips'],
        "budget": float(trip_stats['total_budget'] or 0),
        "wishlist": wish_stats['wishlist_count']
    })

if __name__ == '__main__':
    app.run(debug=True)