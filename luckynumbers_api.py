import pandas as pd
import requests
import random
from datetime import datetime
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

CSV_PATH = 'powerball.csv'



def download_powerball_csv(csv_path):
    """Download the latest Powerball CSV from Texas Lottery website."""
    url = "https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Save the CSV content to the local file
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded and saved {csv_path}")
        return True
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        return False

def load_powerball_data(csv_path):

    #download_powerball_csv(csv_path)
    
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
        print(f"Error loading CSV: {e}")
        return None

def analyze_frequencies(df):
    """Calculate frequency of main numbers and Powerball."""
    main_nums = df[['Num1', 'Num2', 'Num3', 'Num4', 'Num5']].values.flatten()
    main_freq = pd.Series(main_nums).value_counts().to_dict()
    pb_freq = df['Powerball'].value_counts().to_dict()

    # Ensure all possible numbers are included
    main_freq = {i: main_freq.get(i, 0) for i in range(1, 70)}
    pb_freq = {i: pb_freq.get(i, 0) for i in range(1, 27)}
    return main_freq, pb_freq

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

# API Functions.

@app.route('/luckynumbers/ticket=<int:ticket_count>', methods=['GET'])

def api_lucky_numbers(ticket_count):
    if ticket_count < 1 or ticket_count > 100:
        return jsonify({"error": "ticket count must be between 1 and 100"}), 500
    
    if not os.path.exists(CSV_PATH) and not download_powerball_csv(CSV_PATH):
        return jsonify({"error": "Failed to get Powerball data"}), 500

    df = load_powerball_data(CSV_PATH)
    
    if df is None:
        return jsonify({"error": "Failed to get Powerball data"}), 500

    main_freq, pb_freq = analyze_frequencies(df)
    tickets = generate_lucky_numbers(main_freq, pb_freq, ticket_count)

    return jsonify({
        "requested_tickets": ticket_count,
        "lucky_numbers": tickets
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080)

    
    
