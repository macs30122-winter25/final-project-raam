import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect('raam_database.db')
cursor = conn.cursor()

with open('reddit_data_nursing.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    data = list(reader)

table_name = 'nursing_table_raw'
columns = """
timestamp TEXT
,username TEXT
,post_title TEXT
,post_body TEXT
,combined_text TEXT
,score TEXT
,comments_count TEXT
,post_url TEXT
,comment_username TEXT
,comment_body TEXT
,comment_combined_text TEXT
,comment_score TEXT
,comment_timestamp TEXT
"""
create_main_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})'
cursor.execute(create_main_table_query)

placeholders = ', '.join(['?'] * len(header))
insert_query = f'INSERT INTO {table_name} VALUES ({placeholders})'
cursor.executemany(insert_query, data)

create_post_table = """
CREATE TABLE IF NOT EXISTS nursing_posts (
post_id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp TEXT
,username TEXT
,post_title TEXT
,post_body TEXT
,score TEXT
,comments_count TEXT
,post_url TEXT)
"""
cursor.execute(create_post_table)

insert_post_table = """
INSERT INTO nursing_posts (
    timestamp, 
    username, 
    post_title, 
    post_body, 
    score, 
    comments_count, 
    post_url
) 
SELECT DISTINCT 
    timestamp, 
    username, 
    post_title, 
    post_body, 
    score, 
    comments_count, 
    post_url
FROM nursing_table_raw
"""
cursor.execute(insert_post_table)

create_comments_table = """
CREATE TABLE IF NOT EXISTS nursing_comments (
    post_id INTEGER,
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment_username TEXT,
    comment_body TEXT,
    comment_score TEXT,
    comment_timestamp TEXT,
    FOREIGN KEY (post_id) REFERENCES nursing_posts(post_id)
)
"""
cursor.execute(create_comments_table)

insert_comments_table = """
INSERT INTO nursing_comments (
    post_id, 
    comment_username, 
    comment_body, 
    comment_score, 
    comment_timestamp
) 
SELECT 
    p.post_id, 
    t.comment_username, 
    t.comment_body, 
    t.comment_score, 
    t.comment_timestamp
FROM nursing_table_raw t
JOIN nursing_posts p ON t.post_url = p.post_url
"""
cursor.execute(insert_comments_table)

# Cleaning Data
cleaning_comments = """
DELETE FROM nursing_comments
WHERE comment_body = "No Comment" 
OR comment_username = "AutoModerator" 
"""

cursor.execute(cleaning_comments)

conn.commit()
cursor.close()
conn.close()