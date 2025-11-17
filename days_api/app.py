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

    if not data or "first" not in data or "last" not in data:
        return {"error": "Missing required data."}, 400

    elif type(data["first"]) != str or type(data["last"]) != str or "." not in data["first"] or "." not in data["last"]:
        return {"error": "Unable to convert value to datetime."}, 400

    first_date = convert_to_datetime(data["first"])
    second_date = convert_to_datetime(data["last"])
    difference = get_days_between(first_date, second_date)

    add_to_history(request)
    return jsonify({"days": difference}), 200


@app.post("/weekday")
def weekday():
    data = request.json

    if not data:
        return {"error": "Missing required data."}, 400

    elif "date" not in data:
        return {"error": "Missing required data."}, 400

    elif type(data["date"]) != str:
        return {"error": 'Unable to convert value to datetime.'}, 400

    elif "." not in data["date"]:
        return {"error": 'Unable to convert value to datetime.'}, 400

    try:
        date = convert_to_datetime(data["date"])

        add_to_history(request)
        return {"weekday": get_day_of_week_on(date)}, 200

    except ValueError:
        return {"error": 'Unable to convert value to datetime.'}, 400


@app.route("/history", methods=["GET", "DELETE"])
def history():
    if (request.method) == "GET":

        try:
            requested_index = int(request.args.get("number", 5))

        except ValueError:
            return {"error": "Number must be an integer between 1 and 20."}, 400

        if not isinstance(requested_index, int):
            return {"error": "Number must be an integer between 1 and 20."}, 400

        if requested_index <= 0 or requested_index > 21:
            return {"error": "Number must be an integer between 1 and 20."}, 400
        else:
            add_to_history(request)
            return app_history[:requested_index][::-1], 200

    if (request.method) == "DELETE":
        add_to_history(request)
        clear_history()
        return {"status": "History cleared"}, 200


@app.get("/current_age")
def current_age():
    age_date = request.args.get("date")

    if not age_date:
        return {"error": 'Date parameter is required.'}, 400

    elif not isinstance(age_date, str):
        return {"error": "Value for data parameter is invalid."}, 400

    elif "-" not in age_date:
        return {"error": "Value for data parameter is invalid."}, 400

    else:
        try:
            date_class_age = datetime.strptime(age_date, "%Y-%m-%d")
            add_to_history(request)
            return jsonify({"current_age": get_current_age(date_class_age)}), 200
        except ValueError:
            return {"error": "Value for data parameter is invalid."}, 400


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
