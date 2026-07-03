from flask import Flask, jsonify, request
from predictor.fetcher import get_teams, get_matches, get_standings
from predictor.model import predict_match

app = Flask(__name__)

def find_team(teams, name):
    """Find a team by name (case insensitive, partial match)"""
    name_lower = name.lower()
    matches = [t for t in teams if name_lower in t["name"].lower()]
    return matches[0] if matches else None

@app.route("/")
def home():
    return jsonify({
        "message": "World Cup Predictor API",
        "endpoints": {
            "GET /teams": "List all World Cup teams",
            "GET /matches": "List all World Cup matches",
            "GET /standings": "Get current standings", 
            "GET /predict?team1=Brazil&team2=France": "Predict match outcome"
        }
    })

@app.route("/teams")
def teams():
    try:
        data = get_teams()
        return jsonify({"teams": [{"id": t["id"], "name": t["name"]} for t in data]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/matches")
def matches():
    try:
        data = get_matches()
        return jsonify({"matches": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/standings")
def standings():
    try:
        data = get_standings()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict")
def predict():
    team1_name = request.args.get("team1")
    team2_name = request.args.get("team2")

    if not team1_name or not team2_name:
        return jsonify({"error": "Please provide both team1 and team2 query parameters"}), 400

    try:
        teams = get_teams()
        team1 = find_team(teams, team1_name)
        team2 = find_team(teams, team2_name)

        if not team1:
            return jsonify({"error": f"Could not find team: {team1_name}"}), 404
        if not team2:
            return jsonify({"error": f"Could not find team: {team2_name}"}), 404

        prediction = predict_match(team1, team2)
        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)