# Import required packages
import re, sqlite3, time
from selenium import webdriver

# Load chromedriver by giving its full path
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

# Create new connection by creating a new database
conn = sqlite3.connect('IMDB_Movies.db')
c = conn.cursor()

# Create a table called Movies_1 with 15 columns
c.execute("CREATE TABLE IF NOT EXISTS Movies_1 (\
          Title VARCHAR(50), \
          Year VARCHAR(4), \
          Movie_Rating VARCHAR(10), \
          Runtime VARCHAR(10), \
          Genre VARCHAR(30), \
          User_Rating FLOAT(5), \
          Metascore VARCHAR(3), \
          Director VARCHAR(50), \
          Actor_1 VARCHAR(50), \
          Actor_2 VARCHAR(50), \
          Actor_3 VARCHAR(50), \
          Actor_4 VARCHAR(50), \
          User_Votes VARCHAR(10), \
          Gross VARCHAR(10), \
          PRIMARY KEY (Title, Year))")
    
# Create another table called Moves_2 with four columns    
c.execute("CREATE TABLE IF NOT EXISTS Movies_2 (\
          Title VARCHAR(50), \
          Year VARCHAR(4), \
          Plot VARCHAR(500), \
          Top_250 VARCHAR(10))")


