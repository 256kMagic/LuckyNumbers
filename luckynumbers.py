import pandas as pd
import requests
import random
from datetime import datetime
import os

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

def main():
    csv_path = 'powerball.csv'

    # Download the latest CSV
    if not download_powerball_csv(csv_path):
        if not os.path.exists(csv_path):
            print("No local powerball.csv found and download failed. Please check your internet connection or the Texas Lottery website.")
            return
        else:
            print("Using existing local powerball.csv due to download failure.")

    # Load data
    df = load_powerball_data(csv_path)
    if df is None:
        return

    # Analyze frequencies
    main_freq, pb_freq = analyze_frequencies(df)

    # Generate lucky numbers
    try:
        num_tickets = int(input("How many lottery tickets would you like to generate? "))
        if num_tickets < 1:
            raise ValueError("Number of tickets must be positive.")
    except ValueError as e:
        print(f"Invalid input: {e}. Defaulting to 1 ticket.")
        num_tickets = 1

    tickets = generate_lucky_numbers(main_freq, pb_freq, num_tickets)

    # Display results
    print("\nYour Lucky Numbers:")
    for i, (main, pb) in enumerate(tickets, 1):
        print(f"Ticket {i}: {main} Powerball: {pb}")

if __name__ == "__main__":
    main()