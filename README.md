# IMDb Top 250 Scraper

This project scrapes IMDb's Top 250 movies, tracks ranking changes compared to the previous day, and saves the data in a MariaDB database. It also includes a scheduled cron job to automate daily data scraping script.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Running the Code](#running-the-code)
4. [Setting Up the Cron Job](#setting-up-the-cron-job)
5. [MariaDB Setup](#mariadb-setup)
6. [Files Included](#files-included)

---

## Project Overview

This Python-based project fetches IMDb's Top 250 movies and stores the following information:
- Movie title
- Ranking
- URL
- IMDb rating
- Date of scraping
- Ranking change from the previous day

It tracks rank changes and supports flexible storage formats, including JSON and MariaDB.

---

## Setup Instructions

### Setting Up this Environment
1. Clone this repository:
   ```
   git clone https://github.com/Halolage/weiheng-movie-scraping-project.git
   cd movie-scraping-project
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # For MacOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

---

## MariaDB Setup

### Setting Up the Database
1. Start MariaDB service:
   ```
   brew services start mariadb  # macOS
   sudo service mariadb start   # Linux
   ```

2. Log in to MariaDB shell as root:
   ```
   mysql -u root -p
   ```

3. Create the database and user:
   ```
   CREATE DATABASE imdb;

   CREATE USER 'imdb_user'@'localhost' IDENTIFIED BY 'admin';
   GRANT ALL PRIVILEGES ON imdb.* TO 'imdb_user'@'localhost';
   FLUSH PRIVILEGES;
   
4. Create table:
   ```   
   USE imdb;

   CREATE TABLE top_250_movies (
       id INT AUTO_INCREMENT PRIMARY KEY,
       `rank` INT NOT NULL,
       title VARCHAR(255) NOT NULL,
       url VARCHAR(500) NOT NULL,
       rating DECIMAL(3, 1),
       date_scraped DATE,
       rank_change VARCHAR(50)
   );
   ```

---

## Running the Code

1. **Run the Script Manually**:
   Execute the Python script:
   ```
   python src/main.py
   ```

2. The script performs the following tasks:
   - Scrapes IMDb's Top 250 movies.
   - Tracks rank changes compared to the previous day.
   - Saves the data to `imdb_top_250.json`.
   - Stores the data in the MariaDB database.

3. Verify the Database:
   ```
   mysql -u imdb_user -p
   USE imdb;
   SELECT * FROM top_250_movies;
   ```

---

## Setting Up the Cron Job

To automate the script's execution daily at midnight:

1. Open the crontab editor:
   ```
   crontab -e
   ```

2. Add the following line to schedule the job:
   ```
   0 0 * * * /path/to/venv/bin/python /path/to/src/main.py
   ```

3. Verify the cron job:
   ```
   crontab -l
   ```

---

## Files Included

- `src/main.py`: The main script for scraping IMDb and saving data.
- `src/chromedriver`: WebDriver for handling dynamic content.
- `imdb_top_250.json`: Stores the scraped movie data in JSON format.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.
- `imdb_schema.sql`: (Optional) SQL file to set up the database schema.

