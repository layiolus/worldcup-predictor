# World Cup Predictor 

A Python-based World Cup match predictor that uses live data from the [football-data.org](https://football-data.org) API to predict match outcomes, scorelines, and winner confidence for the 2026 FIFA World Cup.

## Features

- **Live data** — pulls real-time team stats, standings, and match history
- **Match prediction** — predicts winner based on team form and standings
- **Scoreline prediction** — generates a realistic scoreline based on goals scored/conceded
- **Confidence rating** — shows how confident the model is in its prediction
- **CLI** — predict matches directly from your terminal
- **REST API** — Flask-powered API for programmatic access to predictions

## Tech Stack

Python, Flask, football-data.org API, python-dotenv, requests

## Setup

1. Clone the repo:
```bash
git clone https://github.com/layiolus/worldcup-predictor.git
cd worldcup-predictor
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Get a free API key from [football-data.org](https://football-data.org) and create a `.env` file:
```bash
echo "FOOTBALL_API_KEY=your_key_here" >> .env
```

## CLI Usage

```bash
# List all World Cup teams
python main.py teams

# Predict a match
python main.py predict Brazil France
python main.py predict "United States" Mexico

# Help
python main.py help
```

## Example CLI Output
╔══════════════════════════════════════════════╗
🏆 WORLD CUP MATCH PREDICTION 🏆
╠══════════════════════════════════════════════╣
Brazil               vs  France
──────────────────────────────────────────────
Prediction Score:
Brazil                13.6
France                17.2
──────────────────────────────────────────────
⚽ Predicted Scoreline: Brazil 1 - 2 France
🏅 Predicted Winner:    France
📊 Confidence:          55.8%
╚══════════════════════════════════════════════╝

## API Usage

Start the server:
```bash
python api.py
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome and endpoint list |
| GET | `/teams` | List all World Cup teams |
| GET | `/matches` | List all World Cup matches |
| GET | `/standings` | Current standings |
| GET | `/predict?team1=Brazil&team2=France` | Predict match outcome |

### Example API Response

```json
{
  "confidence": "55.8%",
  "predicted_scoreline": "Brazil 1 - 2 France",
  "predicted_winner": "France",
  "team1": "Brazil",
  "team1_score": 13.6,
  "team2": "France",
  "team2_score": 17.2
}
```

## Project Structure