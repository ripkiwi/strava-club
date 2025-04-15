## Strava Club Fetcher

**Property of [`ITQ`](https://itq.eu)** </br>
*maintained by `Kevin Burgers`*

---

This Python script fetches the latest activities from a specified Strava Club and exports the data to a clean and structured `.csv` file.

Additionially it creates a `.csv` file with the basis of a leaderboard and visualization thereof for a easy and quick comparison, documenting, or further analysis.

---

**Environment Variables**</br>
Copy `.env.example` to `.env` and fill in your API credentials from: 'https://www.strava.com/settings/api'.</br>

---

**Requirements**</br>
The following script requires:
- python (3.7+)
- requests
- python-dotenv (if using environment variables)

---

**Running the project.**

From the root directory you're able to run:
>python main.py