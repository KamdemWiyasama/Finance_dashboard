from flask import Flask, render_template
from database import init_db
app = Flask(__name__)

@app.route("/")#This is a decorator that defines a route for the web application. The "/" route is the root URL, meaning that when a user accesses the base URL of the application, this function will be executed.
def home():
    return "Finance Dashboard Running"

if __name__ == "__main__":#checks if the script is being run directly (as the main program) and not imported as a module in another script. If this condition is true, the code block under it will be executed.
    init_db()
    app.run(debug=True, use_reloader=False)