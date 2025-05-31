import pandas as pd
import requests
import random
from datetime import datetime, timedelta
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

CSV_PATH = 'powerball.csv'
DOWNLOAD_URL = "https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv"

# Check if the file is missing or older than X hours
def is_file_outdated(filepath, max_age_hours=24):
    """Check if the file is older than max_age_hours or doesn't exist."""
    if not os.path.exists(filepath):
        return True
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    return datetime.now() - file_mod_time > timedelta(hours=max_age_hours)

# Download the file only if needed
def download_powerball_csv(csv_path, force_download=False):
    """Download and overwrite the Powerball CSV only if needed."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    if not force_download and not is_file_outdated(csv_path, max_age_hours=24):
        print(f"[INFO] Using cached Powerball data from {csv_path}")
        return True

    try:
        response = requests.get(DOWNLOAD_URL, headers=headers, timeout=10)
        response.raise_for_status()
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        print(f"[INFO] CSV successfully downloaded and saved to {csv_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to download CSV: {e}")
        return False

# Load the CSV into pandas DataFrame
def load_powerball_data(csv_path):
    """Load and normalize Powerball CSV data."""
    try:
        df = pd.read_csv(csv_path)
        # Ensure consistent column names
        expected_columns = ['Game Name', 'Month', 'Day', 'Year', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Powerball', 'Power Play']
        # Handle missing Power Play column for certain periods
        if 'Power Play' not in df.columns:
            df['Power Play'] = None
        # Reorder columns to match expected format
        df = df.reindex(columns=expected_columns)
        # Convert date components to datetime
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d', errors='coerce')
        return df
    except Exception as e:
        print(f"[ERROR] Error loading CSV: {e}")
        return None

# Analyze frequency of numbers
def analyze_frequencies(df):
    """Calculate frequency of main numbers and Powerball."""
    main_nums = df[['Num1', 'Num2', 'Num3', 'Num4', 'Num5']].values.flatten()
    main_freq = pd.Series(main_nums).value_counts().to_dict()
    pb_freq = df['Powerball'].value_counts().to_dict()

    # Ensure all possible numbers are included
    main_freq = {i: main_freq.get(i, 0) for i in range(1, 70)}
    pb_freq = {i: pb_freq.get(i, 0) for i in range(1, 27)}
    return main_freq, pb_freq

# Generate lucky numbers
def generate_lucky_numbers(main_freq, pb_freq, num_tickets=1):
    """Generate lucky numbers based on frequency weights."""
    main_nums = list(range(1, 70))
    pb_nums = list(range(1, 27))
    main_weights = [main_freq[i] + 1 for i in main_nums]  # +1 to avoid zero weights
    pb_weights = [pb_freq[i] + 1 for i in pb_nums]

    tickets = []
    for _ in range(num_tickets):
        # Weighted random selection for main numbers
        selected_main = random.choices(main_nums, weights=main_weights, k=5)
        # Ensure unique main numbers
        while len(set(selected_main)) < 5:
            selected_main = random.choices(main_nums, weights=main_weights, k=5)
        selected_main = sorted(set(selected_main))
        # Select Powerball
        powerball = random.choices(pb_nums, weights=pb_weights, k=1)[0]
        tickets.append((selected_main, powerball))
    return tickets

# API Endpoint
@app.route('/luckynumbers/ticket=<int:ticket_count>', methods=['GET'])
def api_lucky_numbers(ticket_count):
    if ticket_count < 1 or ticket_count > 100:
        return jsonify({"error": "ticket count must be between 1 and 100"}), 500
    
    # Only download if needed (missing or outdated file)
    if not download_powerball_csv(CSV_PATH, force_download=False):
        return jsonify({"error": "Failed to download latest Powerball data"}), 500

    df = load_powerball_data(CSV_PATH)
    
    if df is None:
        return jsonify({"error": "Failed to load Powerball data"}), 500

    main_freq, pb_freq = analyze_frequencies(df)
    tickets = generate_lucky_numbers(main_freq, pb_freq, ticket_count)

    return jsonify({
        "requested_tickets": ticket_count,
        "lucky_numbers": tickets
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)





