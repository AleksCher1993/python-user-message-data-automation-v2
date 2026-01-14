# User Activity Data Pipeline (Python)

## Overview

This project is a production-style Python data pipeline that collects user and post data from external REST APIs, processes and aggregates the data, and generates analytical reports in JSON and CSV formats.
The main goal of the project is to demonstrate practical skills in:

- working with external APIs

- processing and joining multiple datasets

- building simple ETL-style pipelines

- writing production-ready Python scripts with logging and error handling

The project is intentionally implemented using pure Python, without Pandas or heavy frameworks, to clearly demonstrate core data-processing logic.

## Features

- Fetches data from multiple REST API endpoints

- Caches raw API responses locally in JSON format

- Aggregates and joins data from different sources

- Calculates user activity metrics (posts count per user)

- Generates top-N active users report

- Exports results to JSON and CSV formats

- Implements structured logging

- Handles network, file I/O, and data errors

## Data Sources

The project uses the public JSONPlaceholder API:

- Users: https://jsonplaceholder.typicode.com/users

- Posts: https://jsonplaceholder.typicode.com/posts 


## Project Structure

data/
├── users.json # cached raw users data
├── posts.json # cached raw posts data
├── user_activity.json # processed top active users
├── report_user_activity.csv # CSV report (top users)
├── report_posts_users_list.csv# CSV report (all users)
logs/
├── app.log # application logs
main.py # application entry point
requirements.txt # project dependencies
README.md

## Technologies Used

- Python 3
- requests
- csv
- json
- logging
- os

## How It Works

1. The application starts and initializes logging.

2. It checks whether cached user and post data exist locally.

3. If cached data is missing, it fetches data from external APIs and stores it as JSON files.

4. Posts data is aggregated to calculate how many posts each user has created.

5. Users and posts data are joined into a unified user activity dataset.

6. Top-N most active users are identified.

7. Processed data is saved as JSON and CSV reports.

8. All operations and errors are logged.

## How to Run

1. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

2. Install dependencies:
pip install -r requirements.txt

3. Run the script:
python main.py

## Example Output
After execution, the following files will be generated:

 - data/user_activity.json – normalized user activity data (top active users)

 - data/report_user_activity.csv – CSV report for top users

 - data/report_posts_users_list.csv – CSV report for all users

 - logs/app.log – application logs

## Error Handling and Logging

The application includes:

 - HTTP error handling for API requests

 - File I/O error handling

 - Validation for missing or empty datasets

 - Structured logging for all major execution steps

Logs are written to logs/app.log.

## Possible Improvements

- Add a REST API layer using FastAPI

- Add Docker support for deployment

- Introduce configuration via environment variables (.env)

- Add scheduling (cron / task scheduler)

- Integrate Pandas for advanced analytics

- Add automated tests

## Author

Developed by [AleksBlack]

