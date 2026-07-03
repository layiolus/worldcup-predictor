import requests
from config import BASE_URL, HEADERS, WC_COMPETITION_ID

def get_teams():
    """Fetch all teams in the World Cup"""
    url = f"{BASE_URL}/competitions/{WC_COMPETITION_ID}/teams"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error fetching teams: {response.status_code} - {response.text}")
    return response.json().get("teams", [])

def get_standings():
    """Fetch current World Cup standings"""
    url = f"{BASE_URL}/competitions/{WC_COMPETITION_ID}/standings"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error fetching standings: {response.status_code} - {response.text}")
    return response.json()

def get_matches():
    """Fetch all World Cup matches"""
    url = f"{BASE_URL}/competitions/{WC_COMPETITION_ID}/matches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error fetching matches: {response.status_code} - {response.text}")
    return response.json().get("matches", [])

def get_team_matches(team_id):
    """Fetch recent matches for a specific team"""
    url = f"{BASE_URL}/teams/{team_id}/matches?competitions={WC_COMPETITION_ID}&limit=10"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error fetching team matches: {response.status_code} - {response.text}")
    return response.json().get("matches", [])

def get_team_stats(team_id):
    """Fetch goals scored and conceded by a team in the World Cup"""
    matches = get_team_matches(team_id)
    finished = [m for m in matches if m["status"] == "FINISHED"]

    goals_scored = 0
    goals_conceded = 0
    games_played = 0

    for match in finished:
        home_id = match["homeTeam"]["id"]
        home_goals = match["score"]["fullTime"]["home"]
        away_goals = match["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            goals_scored += home_goals
            goals_conceded += away_goals
        else:
            goals_scored += away_goals
            goals_conceded += home_goals

        games_played += 1

    if games_played == 0:
        return {"avg_scored": 1.2, "avg_conceded": 1.0}

    return {
        "avg_scored": round(goals_scored / games_played, 2),
        "avg_conceded": round(goals_conceded / games_played, 2)
    }