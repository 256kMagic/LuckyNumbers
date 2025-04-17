LuckyNumbers
A Python script to generate Powerball lottery numbers based on historical winning numbers from the Texas Lottery. The script downloads the latest Powerball CSV file, analyzes the frequency of numbers, and generates "lucky" numbers weighted by their past occurrences.
Features

Downloads the latest Powerball winning numbers CSV from the Texas Lottery website.
Handles variable CSV formats (with or without Power Play) from Feb 3, 2010, to the present.
Analyzes the frequency of main numbers (1–69) and Powerball numbers (1–26).
Generates user-specified numbers of lottery tickets with numbers weighted by historical frequency.
Includes error handling for download failures and invalid CSV formats.

Prerequisites

Python 3.6+: Ensure Python is installed on your system.
Dependencies: Install required Python libraries:pip install pandas requests


Git: For cloning and managing the repository.
Internet Connection: Required to download the Powerball CSV.

Installation

Clone the Repository:
git clone https://github.com/256kmagic/LuckyNumbers.git
cd LuckyNumbers

Replace <your-username> with your GitHub username or the repository URL.

Install Dependencies:
pip install pandas requests


Set Up Git (Optional):Configure your Git username and email if you plan to contribute:
git config --global user.name "Your Name"
git config --global user.email "you@example.com"



Usage

Run the Script:
python luckynumbers.py


Follow Prompts:

The script downloads powerball.csv from the Texas Lottery website and saves it in the project directory.
Enter the number of lottery tickets you want to generate when prompted.
The script outputs tickets in the format: [main numbers] Powerball: [powerball].


Example Output:
Successfully downloaded and saved powerball.csv
How many lottery tickets would you like to generate? 2

Your Lucky Numbers:
Ticket 1: [3, 15, 27, 42, 58] Powerball: 12
Ticket 2: [7, 19, 34, 46, 63] Powerball: 8


Notes:

If the CSV download fails, the script uses an existing local powerball.csv if available.
Invalid input for the number of tickets defaults to 1 ticket.



File Structure

luckynumbers.py: Main Python script for downloading, analyzing, and generating lottery numbers.
powerball.csv: Downloaded CSV file containing historical Powerball winning numbers (generated/overwritten on each run).
README.md: This documentation file.

CSV Format
The powerball.csv file follows the Texas Lottery’s format, with variations by date range:

Feb 3, 2010 – Jan 14, 2012: Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball, Power Play
Jan 18, 2012 – Jan 18, 2014: Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball
Jan 22, 2014 – Present: Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Powerball, Power Play

Troubleshooting

Download Errors:
If you see “Error downloading CSV,” check your internet connection or verify the URL: https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv.
Ensure the Texas Lottery website hasn’t changed the CSV location. Visit the site to find the latest URL if needed.


CSV Parsing Errors:
If the CSV format differs from expected, open powerball.csv and check its header. Update the load_powerball_data function in luckynumbers.py if necessary.


Git Issues:
If VS Code prompts for Git credentials, ensure your username and email are set (see Installation step 3).
Clear old credentials in Windows Credential Manager if needed.



Contributing

Fork the Repository: Create a fork on GitHub.
Create a Branch:git checkout -b feature/your-feature


Make Changes: Edit luckynumbers.py or other files.
Commit Changes:git add .
git commit -m "Add your feature"


Push and Create a Pull Request:git push origin feature/your-feature

Open a pull request on GitHub.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or suggestions, contact the maintainer at mike@256kmagic.com or open an issue on GitHub.
