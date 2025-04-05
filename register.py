@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        regno = request.form['regno']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (regno, email, password) VALUES (%s, %s, %s)", (regno, email, password))
        db.commit()
        db.close()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')