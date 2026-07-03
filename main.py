import sys
from predictor.fetcher import get_teams
from predictor.model import predict_match
from predictor.formatter import format_prediction, format_teams_list, format_error

def find_team(teams, name):
    """Find a team by name (case insensitive, partial match)"""
    name_lower = name.lower()
    matches = [t for t in teams if name_lower in t["name"].lower()]
    return matches[0] if matches else None

def list_teams():
    """List all available World Cup teams"""
    print("\nFetching teams...")
    try:
        teams = get_teams()
        print(format_teams_list(teams))
    except Exception as e:
        print(format_error(str(e)))

def predict(team1_name, team2_name):
    """Predict match outcome between two teams"""
    print(f"\nFetching data for {team1_name} vs {team2_name}...")
    try:
        teams = get_teams()
        team1 = find_team(teams, team1_name)
        team2 = find_team(teams, team2_name)

        if not team1:
            print(format_error(f"Could not find team: {team1_name}"))
            return
        if not team2:
            print(format_error(f"Could not find team: {team2_name}"))
            return

        prediction = predict_match(team1, team2)
        print(format_prediction(prediction))

    except Exception as e:
        print(format_error(str(e)))

def print_help():
    print("""
🏆 World Cup Predictor CLI

Usage:
  python main.py teams                        - List all World Cup teams
  python main.py predict <team1> <team2>      - Predict match outcome
  python main.py help                         - Show this help message

Examples:
  python main.py predict Brazil France
  python main.py predict "United States" Mexico
  python main.py teams
""")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print_help()
    elif sys.argv[1] == "teams":
        list_teams()
    elif sys.argv[1] == "predict":
        if len(sys.argv) < 4:
            print(format_error("Please provide two team names. Example: python main.py predict Brazil France"))
        else:
            team1_name = sys.argv[2]
            team2_name = sys.argv[3]
            predict(team1_name, team2_name)
    else:
        print(format_error(f"Unknown command: {sys.argv[1]}"))
        print_help()