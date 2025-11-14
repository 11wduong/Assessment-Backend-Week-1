"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome message."""
    return jsonify({"message": "Welcome to the Days API."}), 200


@app.post("/between")
def between():
    data = request.json

    if "first" not in data or "last" in data:
        return jsonify({"error": "Missing required data."}), 400

    elif not type(data["first"]) == str or not type(data["last"]) == str:
        return jsonify({"error": "Unable to convert value to datetime."}), 400

    elif "." not in data["first"] or "." not in data["last"]:
        return jsonify({"error": "Unable to convert value to datetime."}), 400

    first_date = convert_to_datetime(data["first"])
    second_date = convert_to_datetime(date["last"])
    difference = get_days_between(first_date, second_date)

    return jsonify({"days": (difference).days}), 201


@app.post("/weekday")
def weekday():
    data = request.json

    date = convert_to_datetime(data["date"])

    return get_day_of_week_on(date), 201


@app.route("/history", methods=["GET", "DELETE"])
def history():
    if (request.method) == "GET":
        pass

    if (request.method) == "DELETE":
        pass


@app.get("/current_age")
def current_age():
    age_date = request.args.get("age_date")
    date_class_age = datetime.strptime(age_date, "%Y-%m-%d")
    return jsonify({"current_age": get_current_age(date_class_age)}), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
