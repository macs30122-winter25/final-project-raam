## final-project-raam ##

final-project-raam created by GitHub Classroom

River - zhiyu118

Amrita - amritapathak1

Anita - nitomanto

Mia - mdsowder

## MACS 30122 Final Project: Change in anxiety over the COVID-19 Pandemic on Reddit ##

### Project Overview: ###

We are interested in looking at how health anxiety and general anxiety increased over the pandemic, and what types of anxiety in particular had the most increase. For this project, we scraped data from three subReddits from old.reddit.com: r/HealthAnxiety, r/Nursing, r/Teachers. We scraped posts in these subReddits that fell within the timeframe of January 2019 until the end of December 2021. We suplemented the data from Reddit with data from CDC and WHO surveys relating to anxiety and depression.

### data_processing: ### 
 - create_health_anxiety_tables.py: python file to create raam_database.db
 - create_nursing_tables.py: python file to create raam_database.db
 - create_teaching_tables.py: python file to create raam_database.db

### raw_data: raw data, both scraped and ready-made ###
 - reddit_data: folder containing csvs of scraped data from old.reddit.com
 - who_data.csv: data from WHO survey on COVID-19 related mental health and financial worry
 - Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv: data from CDC during the COVID-19 pandemic related to anxiety and depression

### reports: ###
 - Progress Report 1.pdf: first progress report

### scraping: scraper functions ###
 - find_posts_test.py: python file containing function that searches old.reddit.com subreddit url until the function finds posts that is within a selected time frame (2019-2021)
 - redditscraper_test.py: python file containing function meant to scrape all text information from valid reddit posts on a subreddit

### cdc_eda.ipynb: EDA for the CDC data on anxiety

### metadata.pdf: metadata for the WHO data

### raam_database.db: database containing scraped data from reddit

