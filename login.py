# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE regno = %s", (regno,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['regno']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')