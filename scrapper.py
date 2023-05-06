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
    
# Create another table called Movies_2 with four columns    
c.execute("CREATE TABLE IF NOT EXISTS Movies_2 (\
          Title VARCHAR(50), \
          Year VARCHAR(4), \
          Plot VARCHAR(500), \
          Top_250 VARCHAR(10))")


# Create a dictionary with regex patterns to match and extract the content     
regex_1 = {
    'title': r"<a\s.*?\/title.*?>(.*?)</a>",
    'year': r"<span\s.*\((....)\)</span>",
    'movie_Rating': r"<span\s.*?certificate\">(.*?)</span>",
    'runtime': r"<span\s.*?runtime\">(.*?)\smin</span>",
    'genre': r"<span\s.*?genre\">\s*(.*?)\s*</span>",
    'user_Rating': r"<div\s.*\s.*imdb.*\s.*<strong>(.*?)</strong>",
    'metascore': r"<div\s.*metascore\">\s.*\">(.*?)\s.*\s.*\s.*</div>",
    'director': r"Director:\s*<a[^>]*>([^<]+)</a>",
    'actor_1': r"<a\s.*st_0\">(.*?)</a>",
    'actor_2': r"<a\s.*st_1\">(.*?)</a>",
    'actor_3': r"<a\s.*st_2\">(.*?)</a>",
    'actor_4': r"<a\s.*st_3\">(.*?)</a>",
    'user_Votes': r"<span class=\"text-muted\">Votes:</span>\s*<span name=\"nv\" data-value=\"([\d,]+)\">",
    'gross': r"<span class=\"text-muted\">Gross:</span>\s*<span name=\"nv\" data-value=\"([\d,]+)\">"
}

# Create another dictionary with regex patterns
regex_2 = {
    'title': r"<a\s.*?\/title.*?>(.*?)</a>",
    'year': r"<span\s.*\((....)\)</span>",
    'plot': r"<p class=\"text-muted\">\s*(.*?)\s*</p>",
    'top_250': r"chart/top/.*?>Top 250.*>#(.*?)</span>"
}

# Create a variable to store URL of the websote we are going to scrape, start=$NUM$ in the URL is where $NUM$ value is stored. $NUM starts with 1, and since one webpage has 50 movies listed, the next webpage starts from 51. So we will have to iterate through the pages 20 times.
    
URL = "https://www.imdb.com/search/title/?groups=top_1000&sort=alpha,asc&start=$NUM$&ref_=adv_nxt"

# To iterate 20 times, we will start with 1 and increase 50 after each page, we need to replace $NUM$ in the URL with 1, 51, 101,...and 951. 
for i in range(1,1000,50):
    new_URL = URL.replace("$NUM$", str(i))
    print(new_URL) #to see which webpage we reached and to check the progress of the loop
    driver.get(new_URL) # from selenium library; this will control our browser to interact with web pages we are crawling
    page_content = driver.page_source # Extract HTML source code of the webpage. 
    time.sleep(5) # To pause the iteration for five seconds
    

# Now we will get individual chunk from the list to iterate over it and extract required information.    
    all_chunks = re.compile(r"<div class=\"lister-item-content\">(.*?)</p>\s*</div>\s*</div>",re.S|re.I).findall(page_content)
    
    # Iterate over all the chunks and match the regex patterns from regex_1, since re.findall results in a list of matches, we will store the list in result, and strip and store the first match into a dictionary named data
    for chunk in all_chunks:
        data = {}
        
        for key, regex in regex_1.items():
            result = re.compile(regex, re.S|re.I).findall(chunk)
            
            if result:
                data[key] = result[0].strip()
            else:
                data[key] = None
                
        title, year, movie_Rating, runtime, genre, user_Rating, metascore, director, actor_1, actor_2, actor_3, actor_4, user_Votes, gross = data.values() # Assign dictionary data into variables
        
        # Store the data into Movies_1 table
        query = "INSERT INTO Movies_1 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        c.execute(query, (title, year, movie_Rating, runtime, genre, user_Rating, metascore, director, actor_1, actor_2, actor_3, actor_4, user_Votes, gross))
    
    # This is for extracting plot and top 250 columns. We will store this in table Movies_2    
    for chunk in all_chunks:
        data = {}
        
        for key, regex in regex_2.items():
            result = re.compile(regex,re.S|re.I).findall(chunk)
            
            if result:
                data[key] = result[0].strip()
            else:
                data[key] = None
                
        title, year, plot, top_250 = data.values()
        
        query = "INSERT INTO Movies_2 VALUES (?,?,?,?)"
        c.execute(query, (title, year, plot, top_250))
            
    print(i)


conn.commit()
c.close()
conn.close()