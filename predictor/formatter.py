def format_prediction(prediction):
    """Format prediction dict into a clean CLI-readable string"""
    return f"""
╔══════════════════════════════════════════════╗
        🏆 WORLD CUP MATCH PREDICTION 🏆
╠══════════════════════════════════════════════╣
  {prediction['team1']:<20} vs  {prediction['team2']}
──────────────────────────────────────────────
  Prediction Score:
  {prediction['team1']:<20}  {prediction['team1_score']}
  {prediction['team2']:<20}  {prediction['team2_score']}
──────────────────────────────────────────────
  ⚽ Predicted Scoreline: {prediction['predicted_scoreline']}
  🏅 Predicted Winner:    {prediction['predicted_winner']}
  📊 Confidence:          {prediction['confidence']}
╚══════════════════════════════════════════════╝
""" ##ChatGpt was used to make this "prettier"

def format_teams_list(teams):
    """Format list of teams for CLI display"""
    output = "\n🌍 World Cup Teams:\n"
    output += "─" * 40 + "\n"
    for i, team in enumerate(teams, 1):
        output += f"  {i:>2}. {team['name']}\n"
    return output

def format_error(message):
    """Format error message for CLI display"""
    return f"\n❌ Error: {message}\n"