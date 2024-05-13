import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Dummy user database for demonstration purposes
users = {
    "user1": "password1",
    "user2": "password2"
}

# Function to generate random predicted prices for the given time range
def generate_predicted_prices(start_date, end_date):
    # Calculate the number of days between start and end dates
    num_days = (end_date - start_date).days

    # Generate random prices for the specified time range
    current_price = 50000  # Initial price
    predicted_prices = []
    for _ in range(num_days):
        current_price += random.uniform(-1000, 1000)  # Simulate price change
        predicted_prices.append(round(current_price, 2))  # Round to 2 decimal places

    return predicted_prices

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"
    return render_template("login.html")

# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Dummy user database for demonstration purposes
users = {
    "user1": "password1",
    "user2": "password2"
}

# Function to generate random predicted prices for the given time range
def generate_predicted_prices(start_date, end_date):
    # Calculate the number of days between start and end dates
    num_days = (end_date - start_date).days

    # Generate random prices for the specified time range
    current_price = 50000  # Initial price
    predicted_prices = []
    for _ in range(num_days):
        current_price += random.uniform(-1000, 1000)  # Simulate price change
        predicted_prices.append(round(current_price, 2))  # Round to 2 decimal places

    return predicted_prices

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            return "Username already exists"
        else:
            users[username] = password
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    username = session.get('username')
    if username:
        bitcoin_prices_df = {
            'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'Price': [50000, 51000, 52000]
        }
        return render_template("dashboard.html", username=username, prices=bitcoin_prices_df)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    username = session.get('username')
    if username:
        return render_template("profile.html", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/api/predicted_prices")
def get_predicted_prices():
    # Get the selected time range from the request parameters
    time_range = request.args.get('range')

    # Define start and end dates for the selected time range
    start_date = datetime(2024, 4, 20)
    if time_range == '1year':
        end_date = start_date + timedelta(days=365)
    elif time_range == '6months':
        end_date = start_date + timedelta(days=365 / 2)
    elif time_range == '3months':
        end_date = start_date + timedelta(days=365 / 4)
    elif time_range == '1month':
        end_date = start_date + timedelta(days=30)
    elif time_range == '7days':
        end_date = start_date + timedelta(days=7)
    elif time_range == '1day':
        end_date = start_date + timedelta(days=1)
    else:
        return jsonify(error="Invalid time range")

    # Generate predicted prices for the specified time range
    predicted_prices = generate_predicted_prices(start_date, end_date)

    # Generate dates for the predicted prices
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(len(predicted_prices))]

    # Return predicted prices and dates as JSON response
    return jsonify(prices=predicted_prices, dates=dates)

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)
