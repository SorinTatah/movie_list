import sqlite3
from movies_list import movie_list

connection = sqlite3.connect("movies.db")

#communicate with the data base using a cursor object
cursor = connection.cursor()
query_data = """ CREATE TABLE movies (
    id integer PRIMARY KEY,
    Release_Date integer,
    Movie_Name text,
    Watched_Status text
)"""
cursor.execute(query_data)
cursor.executemany("INSERT INTO movies (id, Release_Date, Movie_Name, Watched_Status) VALUES (:id, :Release_Date, :Movie_Name, :Watched_Status)", movie_list)
connection.commit()

connection.close()