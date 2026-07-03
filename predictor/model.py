from predictor.fetcher import get_team_matches, get_standings, get_team_stats

def get_team_form(matches, team_id):
    """Calculate form score based on last 5 matches (W=3, D=1, L=0)"""
    form_score = 0
    recent = [m for m in matches if m["status"] == "FINISHED"][-5:]
    
    for match in recent:
        home_id = match["homeTeam"]["id"]
        away_id = match["awayTeam"]["id"]
        home_goals = match["score"]["fullTime"]["home"]
        away_goals = match["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            if home_goals > away_goals:
                form_score += 3
            elif home_goals == away_goals:
                form_score += 1
        elif team_id == away_id:
            if away_goals > home_goals:
                form_score += 3
            elif home_goals == away_goals:
                form_score += 1

    return form_score

def get_standing_score(standings_data, team_id):
    """Get a score based on standings position — higher position = higher score"""
    try:
        groups = standings_data.get("standings", [])
        for group in groups:
            for entry in group.get("table", []):
                if entry["team"]["id"] == team_id:
                    position = entry["position"]
                    points = entry["points"]
                    goal_diff = entry["goalDifference"]
                    return points * 2 + goal_diff - position
    except Exception:
        pass
    return 0

def predict_scoreline(team1_stats, team2_stats):
    """
    Predict scoreline based on average goals scored vs conceded.
    team1 expected goals = avg team1 scored vs avg team2 conceded
    """
    team1_expected = round((team1_stats["avg_scored"] + team2_stats["avg_conceded"]) / 2)
    team2_expected = round((team2_stats["avg_scored"] + team1_stats["avg_conceded"]) / 2)
    return team1_expected, team2_expected

def predict_match(team1, team2):
    """
    Predict match outcome between two teams.
    Returns a dict with team names, scores, scoreline and predicted winner.
    """
    team1_id = team1["id"]
    team2_id = team2["id"]
    team1_name = team1["name"]
    team2_name = team2["name"]

    # Get form
    try:
        team1_matches = get_team_matches(team1_id)
        team1_form = get_team_form(team1_matches, team1_id)
    except Exception:
        team1_form = 0

    try:
        team2_matches = get_team_matches(team2_id)
        team2_form = get_team_form(team2_matches, team2_id)
    except Exception:
        team2_form = 0

    # Get standings score
    try:
        standings = get_standings()
        team1_standing = get_standing_score(standings, team1_id)
        team2_standing = get_standing_score(standings, team2_id)
    except Exception:
        team1_standing = 0
        team2_standing = 0

    # Get team stats for scoreline
    try:
        team1_stats = get_team_stats(team1_id)
    except Exception:
        team1_stats = {"avg_scored": 1.2, "avg_conceded": 1.0}

    try:
        team2_stats = get_team_stats(team2_id)
    except Exception:
        team2_stats = {"avg_scored": 1.2, "avg_conceded": 1.0}

    # Final score — weighted combination of form and standings
    team1_score = (team1_form * 0.6) + (team1_standing * 0.4)
    team2_score = (team2_form * 0.6) + (team2_standing * 0.4)

    # Predict scoreline
    team1_goals, team2_goals = predict_scoreline(team1_stats, team2_stats)

    # Align scoreline with predicted winner
    if team1_score > team2_score and team1_goals <= team2_goals:
        team1_goals = team2_goals + 1
    elif team2_score > team1_score and team2_goals <= team1_goals:
        team2_goals = team1_goals + 1

    # Determine winner
    if team1_score > team2_score:
        winner = team1_name
        confidence = round((team1_score / (team1_score + team2_score + 0.01)) * 100, 1)
    elif team2_score > team1_score:
        winner = team2_name
        confidence = round((team2_score / (team1_score + team2_score + 0.01)) * 100, 1)
    else:
        winner = "Draw"
        confidence = 50.0

    return {
        "team1": team1_name,
        "team2": team2_name,
        "team1_score": round(team1_score, 2),
        "team2_score": round(team2_score, 2),
        "predicted_winner": winner,
        "confidence": f"{confidence}%",
        "predicted_scoreline": f"{team1_name} {team1_goals} - {team2_goals} {team2_name}"
    }