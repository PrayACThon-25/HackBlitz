from flask import Flask, render_template, request, session, flash, redirect, url_for
import google.generativeai as genai
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from pillRemainder import pill_blueprint
from appointmentScheduler import appointment_blueprint
from bookAppointment import book_appointment_blueprint
from diatPlanner import diet_blueprint
from diseasePrediction import disease_blueprint

app = Flask(__name__)
app.secret_key = 'healthmate_secret_key'

# MongoDB configuration
def get_db():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client.healthmate
        # Create unique index for regno if it doesn't exist
        db.users.create_index('regno', unique=True)
        return db
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['password']

        try:
            db = get_db()
            if not db:
                flash('Database connection error')
                return render_template('login.html')

            user = db.users.find_one({'regno': regno})

            if user and check_password_hash(user['password'], password):
                session['user'] = user['regno']
                session['email'] = user['email']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid registration number or password')
        except Exception as e:
            flash(f'Login error: {str(e)}')
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        regno = request.form['regno']
        email = request.form['email']
        password = request.form['password']

        if not all([regno, email, password]):
            flash('All fields are required')
            return render_template('register.html')

        try:
            db = get_db()
            if not db:
                flash('Database connection error')
                return render_template('register.html')

            # Check if user already exists
            if db.users.find_one({'$or': [{'regno': regno}, {'email': email}]}):
                flash('Registration number or email already exists')
                return render_template('register.html')

            # Hash password and create user
            hashed_password = generate_password_hash(password)
            db.users.insert_one({
                'regno': regno,
                'email': email,
                'password': hashed_password,
                'created_at': datetime.datetime.utcnow()
            })

            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration error: {str(e)}')
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Protected route example
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Configure Gemini API
genai.configure(api_key="AIzaSyA2byhZ6SP-ychVIeye29Qsc8iH6q9hIwo")
model = genai.GenerativeModel("gemini-1.5-flash")

# Register blueprints
app.register_blueprint(pill_blueprint)
app.register_blueprint(appointment_blueprint)
# Add this line with your other blueprint registrations
app.register_blueprint(book_appointment_blueprint)
app.register_blueprint(diet_blueprint)
app.register_blueprint(disease_blueprint)

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    messages = []
    if request.method == "POST":
        user_input = request.form["message"]
        messages.append(("You", user_input))
        try:
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = f"❌ HealthMate AI Error: {str(e)}"
        messages.append(("HealthMate AI", bot_reply))
    return render_template("chat.html", messages=messages)
#krishna code
def query_openrouter(symptoms):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-70b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a highly intelligent medical assistant. Given symptoms, provide possible conditions, risks, and general advice. Be specific and concise."
            },
            {
                "role": "user",
                "content": symptoms
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process that. Please try again."

if __name__ == "__main__":
    app.run(debug=True)