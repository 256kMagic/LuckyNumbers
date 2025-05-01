# LuckyNumbers

A Python 3 script that generates Powerball lottery numbers using historical winning numbers from the Texas Lottery. The script downloads the latest Powerball CSV file, analyzes number frequencies, and generates "lucky" numbers weighted by their past occurrences.

## Features
- Downloads the latest `powerball.csv` from the Texas Lottery website.
- Supports variable CSV formats (with or without Power Play) from February 3, 2010, to the present.
- Analyzes frequencies of main numbers (1–69) and Powerball numbers (1–26).
- Generates user-specified numbers of lottery tickets with weighted random selection.
- Handles errors for download failures and invalid CSV formats.

## Prerequisites
- **Python 3**: Install from [python.org](https://www.python.org/downloads/). Ensure `python3` is available in your command line.
- **Git**: Install from [git-scm.com](https://git-scm.com/download/win) for repository management.
- **Internet Connection**: Required to download the Powerball CSV.
- **Dependencies for Script**: Python 3 libraries `pandas` and `requests`.
- **Dependencies for API**: Python 3 libraries `pandas`, `requests` and `flask`.


## Installation
**Dependencies Installation**
```bash
pip install -r requirements.txt
```

**No** installation steps are required beyond ensuring prerequisites are met. Place `luckynumbers.py` in your project directory (e.g., `C:\Users\yourname\Projects\LuckyNumbers`) and run it as described in [Usage](#usage).

## Usage
### Script
1. **Run the Script**:
   ```bash
   python3 luckynumbers.py
   ```

2. **Follow Prompts**:
   - The script downloads `powerball.csv` from the Texas Lottery and saves it locally.
   - Enter the number of lottery tickets to generate when prompted.
   - Output shows tickets in the format: `[main numbers] Powerball: [powerball]`.

3. **Example Output**:
   ```
   Successfully downloaded and saved powerball.csv
   How many lottery tickets would you like to generate? 2

   Your Lucky Numbers:
   Ticket 1: [3, 15, 27, 42, 58] Powerball: 12
   Ticket 2: [7, 19, 34, 46, 63] Powerball: 8
   ```

4. **Notes**:
   - If the CSV download fails, the script uses an existing local `powerball.csv` if available.
   - Invalid input for ticket count defaults to 1 ticket.
### API Usage
**EndPoint**
```bash
GET /luckynumbers/ticket=<number_of_tickets>
```
**Parameters**
`<number_of_tickets>` – Number of lottery tickets to generate (integer between 1 and 100)
**Example Request**
```bash
GET http://<IP_ADDRESS>:8080/luckynumbers/ticket=5
```
**Example Response**
```json
{
  "requested_tickets": 5,
  "lucky_numbers": [
    { "main": [8, 15, 23, 34, 59], "powerball": 12 },
    { "main": [4, 11, 19, 26, 61], "powerball": 7 }
  ]
}
```

## File Structure
- `luckynumbers.py`: Core script for downloading, analyzing, and generating numbers.
- `luckynumbers_api.py` : API Script using a Flash App.
- `requirements.txt`: Text file specifying the required dependencies.
- `powerball.csv`: Downloaded CSV with historical Powerball data (overwritten on each run).
- `README.md`: This documentation file.

## CSV Format
The `powerball.csv` file follows the Texas Lottery format:
- **Feb 3, 2010 – Jan 14, 2012**: `Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball, Power Play`
- **Jan 18, 2012 – Jan 18, 2014**: `Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball`
- **Jan 22, 2014 – Present**: `Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball, Power Play`

## Troubleshooting

- **Download Errors**:
  - If you see `Error downloading CSV`, check your internet connection or the URL:
    ```
    https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv
    ```
  - Visit [texaslottery.com](https://www.texaslottery.com) to confirm the CSV URL if it has changed.

- **CSV Parsing Errors**:
  - If the CSV fails to load, open `powerball.csv` in a text editor and verify its header matches the expected format.
  - Update the `load_powerball_data` function in `luckynumbers.py` if the format differs.

## Contributing

1. **Fork the Repository**: Create a fork on GitHub.
2. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make Changes**: Edit files (e.g., `luckynumbers.py`).
4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Add your feature"
   ```
5. **Push and Create Pull Request**:
   ```bash
   git push origin feature/your-feature
   ```
   Open a pull request on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or suggestions, contact Mike at `mike@256kmagic.com` or open an issue on GitHub.
