**Strava Club Fetcher**

This Python script fetches the latest activities from a specified Strava Club and exports the data to a clean and structured `.csv` file.

Additionially it creates a `.csv` file with the basis of a leaderboard and visualization thereof for a easy and quick comparison, documenting, or further analysis.

With the new Strava API lacking essential attributes such as `start_date` and `activity_id`, this makes it so you can save all activities in your club and identify them uniquely due to the added `unique_id` tag.

---

**Environment Variables**</br>
Copy `.env.example` to `.env` and fill in your API credentials from: 'https://www.strava.com/settings/api'.</br>

---

**Requirements**</br>
The following script requires:
- python (3.7+)
- requests
- python-dotenv

---

**Running the project.**

From the root directory you're able to run:

>python main.py

All outputted files will be found in the newly created `./output/` directories.