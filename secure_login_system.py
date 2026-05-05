from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pyotp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 🗄️ Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False)


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔐 Hash password
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        # 🔑 Generate OTP secret
        otp_secret = pyotp.random_base32()

        user = User(username=username, password=hashed_pw, otp_secret=otp_secret)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['temp_user'] = user.id
            return redirect('/verify-otp')

        return "Invalid credentials"

    return render_template('login.html')


# 🔐 OTP Verification (2FA)
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        user = User.query.get(session.get('temp_user'))

        totp = pyotp.TOTP(user.otp_secret)

        if totp.verify(otp):
            session['user_id'] = user.id
            return redirect('/dashboard')

        return "Invalid OTP"

    return '''
        <form method="POST">
            Enter OTP: <input name="otp">
            <button type="submit">Verify</button>
        </form>
    '''


# 🏠 Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return "Welcome! You are logged in securely ✅"


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# 🚀 Run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
