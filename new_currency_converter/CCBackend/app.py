from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")

app.secret_key = b'^\x06\x84\xd3d\xf7\xe6\t\xf7\xd8~\x86\xb0Q\xf4\xc0\xf0\x8c\xfc\x14\x8f\x15\xdc\x0b'
# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route("/check_users")
def check_users():
    users = User.query.all()

    num_users = len(users)

    user_details = [{"username": user.username, "password":user.password} for user in users]

    return f"Number of users: {num_users} <br> User Details: {user_details}"

# Create database tables
with app.app_context():
    db.create_all()

# Redirect root URL to Login Page
@app.route("/")
def home():
    return redirect(url_for("login"))

# Route for the Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            return redirect(url_for("index"))
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template("login.html")

# Route for the Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create and save new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# Route for the Home Page (Currency Converter)
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user session data (or whatever you use for user login)
    return redirect(url_for('login')) 

# API Route for Currency Conversion
@app.route("/convert", methods=["POST"])
def convert_currency():
    data = request.json
    amount = data.get("amount")
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")

    try:
         amount = float(amount)

         # Dummy conversion rates for demonstration
         conversion_rates = {
               "USD": {"INR": 82.5, "EUR": 0.92, "GBP": 0.73, "JPY": 131.7, "AUD": 1.5, "CAD": 1.35, "CHF": 0.94, "CNY": 6.8, "NZD": 1.6, "SGD": 1.36, "ZAR": 18.2, "KRW": 1300, "BRL": 5.2, "MXN": 18.5},
               "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0088, "JPY": 1.6, "AUD": 0.018, "CAD": 0.016, "CHF": 0.012, "CNY": 0.082, "NZD": 0.019, "SGD": 0.016, "ZAR": 0.22, "KRW": 15.7, "BRL": 0.062, "MXN": 0.22},
               "EUR": {"USD": 1.09, "INR": 89.7, "GBP": 0.79, "JPY": 143.2, "AUD": 1.63, "CAD": 1.47, "CHF": 1.02, "CNY": 7.39, "NZD": 1.74, "SGD": 1.48, "ZAR": 19.8, "KRW": 1432, "BRL": 5.8, "MXN": 19.9},
               "GBP": {"USD": 1.36, "INR": 102.5, "EUR": 1.27, "JPY": 181.3, "AUD": 2.06, "CAD": 1.86, "CHF": 1.29, "CNY": 8.7, "NZD": 2.2, "SGD": 1.85, "ZAR": 26.2, "KRW": 1934, "BRL": 7.5, "MXN": 26.6},
               "JPY": {"USD": 0.0076, "INR": 0.62, "EUR": 0.007, "GBP": 0.0055, "AUD": 0.011, "CAD": 0.009, "CHF": 0.007, "CNY": 0.061, "NZD": 0.013, "SGD": 0.011, "ZAR": 0.14, "KRW": 10.7, "BRL": 0.041, "MXN": 0.15},
               "AUD": {"USD": 0.67, "INR": 55.4, "EUR": 0.61, "GBP": 0.49, "JPY": 92.7, "CAD": 0.89, "CHF": 0.62, "CNY": 4.52, "NZD": 1.08, "SGD": 0.91, "ZAR": 13.2, "KRW": 869, "BRL": 3.64, "MXN": 12.1},
               "CAD": {"USD": 0.74, "INR": 61.1, "EUR": 0.68, "GBP": 0.54, "JPY": 108.4, "AUD": 1.12, "CHF": 0.7, "CNY": 5.36, "NZD": 1.21, "SGD": 1.05, "ZAR": 14.8, "KRW": 1025, "BRL": 4.2, "MXN": 13.4},
               "CHF": {"USD": 1.07, "INR": 88.5, "EUR": 0.98, "GBP": 0.77, "JPY": 138.7, "AUD": 1.61, "CAD": 1.43, "CNY": 7.66, "NZD": 1.76, "SGD": 1.49, "ZAR": 19.9, "KRW": 1423, "BRL": 6.5, "MXN": 21.6},
               "CNY": {"USD": 0.15, "INR": 12.3, "EUR": 0.14, "GBP": 0.11, "JPY": 16.3, "AUD": 0.22, "CAD": 0.19, "CHF": 0.13, "NZD": 0.24, "SGD": 0.19, "ZAR": 2.6, "KRW": 201, "BRL": 0.85, "MXN": 3.1},
               "NZD": {"USD": 0.63, "INR": 51.5, "EUR": 0.58, "GBP": 0.46, "JPY": 79.4, "AUD": 0.93, "CAD": 0.83, "CHF": 0.57, "CNY": 4.1, "SGD": 0.85, "ZAR": 12.2, "KRW": 853, "BRL": 3.38, "MXN": 11.4},
               "SGD": {"USD": 0.74, "INR": 61.7, "EUR": 0.68, "GBP": 0.54, "JPY": 107.7, "AUD": 1.1, "CAD": 0.95, "CHF": 0.67, "CNY": 5.33, "NZD": 1.17, "ZAR": 13.6, "KRW": 1000, "BRL": 4.3, "MXN": 14.1},
               "ZAR": {"USD": 0.055, "INR": 4.7, "EUR": 0.053, "GBP": 0.038, "JPY": 7.1, "AUD": 0.075, "CAD": 0.068, "CHF": 0.05, "CNY": 0.38, "NZD": 0.082, "SGD": 0.073, "KRW": 72.3, "BRL": 0.31, "MXN": 1.1},
               "KRW": {"USD": 0.00076, "INR": 0.63, "EUR": 0.00072, "GBP": 0.00052, "JPY": 0.093, "AUD": 0.0011, "CAD": 0.00097, "CHF": 0.0007, "CNY": 0.005, "NZD": 0.0013, "SGD": 0.001, "ZAR": 0.014, "BRL": 0.062, "MXN": 0.23},
               "BRL": {"USD": 0.19, "INR": 16.1, "EUR": 0.17, "GBP": 0.13, "JPY": 24.5, "AUD": 0.28, "CAD": 0.24, "CHF": 0.15, "CNY": 1.17, "NZD": 0.3, "SGD": 0.23, "ZAR": 3.3, "KRW": 16.1, "MXN": 5.6},
               "MXN": {"USD": 0.054, "INR": 4.5, "EUR": 0.053, "GBP": 0.037, "JPY": 6.6, "AUD": 0.083, "CAD": 0.075, "CHF": 0.051, "CNY": 0.32, "NZD": 0.087, "SGD": 0.071, "ZAR": 0.91, "KRW": 4.4, "BRL": 0.18}
          }

         if from_currency not in conversion_rates or to_currency not in conversion_rates[from_currency]:
               return jsonify({"error": "Conversion rate not available"}), 400

         converted_amount = amount * conversion_rates[from_currency][to_currency]
         return jsonify({"converted_amount": converted_amount})

    except ValueError:
         return jsonify({"error": "Invalid amount Please enter a numeric value"}), 400

if __name__ == "__main__":
    app.run(debug=True)


