from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
from database import init_db
import sqlite3
import os

print(os.path.abspath("database.db"))

app = Flask(__name__)



@app.route("/convert", methods=["GET"])
def convert_currency():
    conn= sqlite3.connect("database.db")
    cursor= conn.cursor()
    
    try:
        amount= request.args.get("amount", type=float)
        from_currency= request.args.get("from", default="USD", type=str)
        from_currency = from_currency.upper()
        to_currency = request.args.get("to", default="EUR", type=str)
        to_currency = to_currency.upper()

        if amount is None or not from_currency  or not to_currency:
            return jsonify({"error": "Missing required parameters."}), 400
        
        if amount<=0:
            return jsonify({"error": 'Amount must be greater than zero.'})
        
        API_KEY = "957a7516a61c51c5a598bf2e6d0b1acc"
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}&access_key={API_KEY}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch exchange rate"}), 502

        data = response.json()

        print(data)
        if "result" not in data:
            return jsonify({"error": "Invalid response from exchange rate API."}), 500
        
        result = data["result"]

        result = round(result, 2)

        return jsonify({"converted" : result})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Exchange rate API request timed out."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@app.route("/add", methods=["POST"])#This route is defined to handle POST requests to the "/add" URL. When a user submits the form on the webpage, the data will be sent to this route for processing.
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]

    conn = sqlite3.connect("database.db")
    cursor= conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", 
        (category, amount, date)
    )
    
    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/")
def home():
    
    conn= sqlite3.connect("database.db")
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    conn.close()
    print(expenses)
    return render_template("index.html", expenses=expenses)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)