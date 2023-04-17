#Step 1, get classes required from audit
#Step 2, search for classes that fit criteria, add to DB
#Step 3, find score for each teach for each top class in class DB

#Step 2, Atlast:
def atlasMajor(major= "Computer Engineering BSE"): #need to change it so major is in a seperate table and it shares integer key with classes table
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import sqlite3
    import re
    import os
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    majorURL = major.replace(' ','%20')
    url = 'https://atlas.ai.umich.edu/major/'+majorURL
    # Set the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\gecko\Downloads\chromedriver_win32 (4)\chromedriver.exe"

    # Initialize a Chrome webdriver instance
    driver = webdriver.Chrome(chromedriver_path)

    driver.get(url)

    element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "myNavbar"))
        )
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    course_container = soup.find('div', class_ = 'common-courses-container')
    links = []
    for link in course_container.find_all('a'):
        links.append(link.get('href'))
    links = [x for x in links if x is not None and '/bookmark/' not in x]
    counter = 0
    if len(links)>0:
        for url in links:
            if counter >= 25:
                break
            try:
                driver.get('https://atlas.ai.umich.edu'+url)

                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*")))

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find the span element with class 'bold blue-highlight-text'
                median_grade_span = soup.find('span', class_='bold blue-highlight-text')
                median_grade = median_grade_span.text


                title_element = soup.find('title')
                title = title_element.text
            except:
                time.sleep(10)
                print('error #1')
                driver.refresh()

            try:
                element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, "course-eval-card-container"))
                )

                elements = driver.find_elements(by = By.CLASS_NAME, value="course-eval-card-container")

                count = 0
                for element in elements:
                    if  count == 0:
                        desire = element.text
                        desire = re.search(r'\b\d+\b', desire).group(0)
                        count += 1
                    elif count == 1:
                        understanding = element.text
                        understanding = re.search(r'\b\d+\b', understanding).group(0)
                        count += 1
                    elif count == 2:
                        workload = element.text
                        workload = re.search(r'\b\d+\b', workload).group(0)
                        count += 1
                    elif count == 3:
                        expectation = element.text
                        expectation = re.search(r'\b\d+\b', expectation).group(0)
                        count += 1
                    elif count == 4:
                        interest = element.text
                        interest = re.search(r'\b\d+\b', interest).group(0)
                #print('\n',title, median_grade, desire, understanding, workload, expectation, interest)

                # Connect to the database
                path = os.path.dirname(os.path.abspath(__file__))
                conn = sqlite3.connect(path+'/'+'database.db')

                # Create a cursor object
                cursor = conn.cursor()

                # Create the table if it does not exist
                cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS classes
                (id INTEGER PRIMARY KEY, title TEXT, major_id INTEGER, median_grade TEXT, workload INTEGER, understanding INTEGER, desire INTEGER, expectation INTEGER, interest INTEGER)
                ''')
                cursor.execute('CREATE TABLE IF NOT EXISTS major (id INTEGER PRIMARY KEY, major TEXT)')
                try:
                    # Check if the location already exists in the job locations table
                    cursor.execute('SELECT id FROM major WHERE major=?', (major,))
                    result = cursor.fetchone()
                    if result is not None:
                        # Use the existing job location ID
                        major_id = result[0]
                    else:
                        # Insert the job location into the job locations table
                        cursor.execute('INSERT INTO major (major) VALUES (?)', (major,))
                        major_id = cursor.lastrowid
                except KeyError:
                    major_id = None
                    major_id = None

                cursor.execute(f'''
                    INSERT OR IGNORE INTO classes (title, major_id, median_grade, workload, understanding, desire, expectation, interest)
                    SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM classes WHERE title=?)
                    ''', (title, major_id, median_grade, workload, understanding, desire, expectation, interest, title))
                conn.commit()

    
                if cursor.rowcount >= 1:
                    counter += 1

                cursor.close()
                conn.close()
            except:
                path = os.path.dirname(os.path.abspath(__file__))
                conn = sqlite3.connect(path+'/'+'database.db')

                # Create a cursor object
                cursor = conn.cursor()

                # Create the table if it does not exist
                cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS classes
                (id INTEGER PRIMARY KEY, title TEXT, major_id INTEGER, median_grade TEXT, workload INTEGER, understanding INTEGER, desire INTEGER, expectation INTEGER, interest INTEGER)
                ''')
                cursor.execute('CREATE TABLE IF NOT EXISTS major (id INTEGER PRIMARY KEY, major TEXT)')
                try:
                    # Check if the location already exists in the job locations table
                    cursor.execute('SELECT id FROM major WHERE major=?', (major,))
                    result = cursor.fetchone()
                    if result is not None:
                        # Use the existing job location ID
                        major_id = result[0]
                    else:
                        # Insert the job location into the job locations table
                        cursor.execute('INSERT INTO major (major) VALUES (?)', (major,))
                        major_id = cursor.lastrowid
                except KeyError:
                    major_id = None
                    major_id = None

                cursor.execute(f'''
                    INSERT OR IGNORE INTO classes (title,major_id, median_grade)
                    SELECT ?,?,? WHERE NOT EXISTS (SELECT 1 FROM classes WHERE title=?)
                    ''', (title, major_id, median_grade, title))
                conn.commit()
                if cursor.rowcount >= 1:
                    counter += 1

                cursor.close()
                conn.close()            
        
        driver.quit()

    else:
        print('please input an alternative major, or ensure the major you inputted is correct')

import sqlite3

def convertGrades():
    # Define a function to convert the grade letter to a 4.0 scale grade
    def convert_grade(grade_letter):
        if grade_letter == 'A+' or grade_letter == 'A':
            return 4.0
        elif grade_letter == 'A-':
            return 3.7
        elif grade_letter == 'B+':
            return 3.3
        elif grade_letter == 'B':
            return 3.0
        elif grade_letter == 'B-':
            return 2.7
        elif grade_letter == 'C+':
            return 2.3
        elif grade_letter == 'C':
            return 2.0
        elif grade_letter == 'C-':
            return 1.7
        elif grade_letter == 'D+':
            return 1.3
        elif grade_letter == 'D':
            return 1.0
        else:
            return 'N/A'

    # Define a SQL query to update the "median_grade" column to a 4.0 scale grade
    sql_query = '''
    UPDATE classes
    SET median_grade = ?
    WHERE id = ?
    '''

    # Open a connection to the database
    conn = sqlite3.connect('database.db')

    # Get a cursor object for the database connection
    cursor = conn.cursor()

    # Execute the SQL query to get all rows in the "classes" table
    cursor.execute('SELECT id, median_grade FROM classes')
    rows = cursor.fetchall()

    # Iterate over all rows in the "classes" table and update each one
    for row in rows:
        grade_4scale = convert_grade(row[1])
        cursor.execute(sql_query, (grade_4scale, row[0]))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def majorAvg(column_name):
    import sqlite3
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Connect to the SQL database
    conn = sqlite3.connect('database.db')

    # Retrieve data from the SQL table
    df = pd.read_sql_query('SELECT * FROM classes', conn)
    majors = pd.read_sql_query('SELECT * FROM major', conn)

    # Join the two tables on major_id
    joined_df = pd.merge(df, majors, left_on='major_id', right_on='id')

    # Compute the average value per unique major_id
    joined_df[column_name] = pd.to_numeric(joined_df[column_name], errors='coerce')
    mean_values = joined_df.groupby(['major_id', 'major'])[column_name].mean().reset_index()

    # Plot the mean values for each major
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(mean_values['major'], mean_values[column_name])
    ax.set_xlabel('Major Name')
    ax.set_ylabel('Mean ' + column_name.capitalize())
    ax.set_title('Mean ' + column_name.capitalize() + ' per Major Name')
    plt.xticks(rotation=0)
    plt.show()




def GPTsalary(major = 'Computer Engineering BSE'):
    import openai
    import re
    openai.api_key = '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'

    # Set the prompt for the OpenAI API
    prompt = ("Create a 5 bulletpoint list of job titles an individual with a major in  " + major + " would normally have")

    # Generate a response using the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated message from the API response
    message = response.choices[0].text.strip()
    output = []
    for line in message.split('\n'):
        line =  re.sub(r'^[^a-zA-Z]+', '', line)
        line = line.strip()
        output.append(line)
    return major, output



def salary(jobTupl = ('Computer Engineering BSE', ['Computer Engineer', 'Software Engineer', 'Hardware Engineer', 'Network Engineer', 'Systems Engineer'])):
    import http.client
    import sqlite3
    import json
    import re

    host = 'jooble.org'
    key = '5d5716ba-8dec-4784-b885-926a7ebee49f'

    connection = http.client.HTTPConnection(host)
    #request headers
    headers = {"Content-type": "application/json"}
    #json query
    counter = 0
    major = jobTupl[0]
    for jobM in jobTupl[1]:
        if counter >= 25:
                    break
        for x in range(1,5): #this gets 4 pages of listings per job
            if counter >= 25:
                    break
            body = '{ "keywords": "'+jobM+'", "location": "US", "page": '+str(x)+', "salary": "10" }' #this limit isint working
            connection.request('POST','/api/' + key, body, headers)
            response = connection.getresponse()
            data = response.read().decode("utf-8")
            json_data = json.loads(data)

            #print(json_data)

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            # Create the table if it doesn't already exist
            c.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, major_id INTEGER, job_location_id INTEGER, snippet TEXT, salary TEXT, company TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS major (id INTEGER PRIMARY KEY, major TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS job_locations (id INTEGER PRIMARY KEY, location TEXT)')
            # Loop through the jobs and insert them into the database
            for job in json_data['jobs']:
                if counter >= 25:
                    break
                try:
                    # Check if the location already exists in the job locations table
                    c.execute('SELECT id FROM major WHERE major=?', (major,))
                    result = c.fetchone()
                    if result is not None:
                        # Use the existing job location ID
                        major_id = result[0]
                    else:
                        # Insert the job location into the job locations table
                        c.execute('INSERT INTO major (major) VALUES (?)', (major,))
                        major_id = c.lastrowid
                except KeyError:
                    major_id = None
                    major_id = None
                try:
                    title = job['title']
                except KeyError:
                    title = None
                
                try:
                    job_location = job['location']
                    # Check if the location already exists in the job locations table
                    c.execute('SELECT id FROM job_locations WHERE location=?', (job_location,))
                    result = c.fetchone()
                    if result is not None:
                        # Use the existing job location ID
                        job_location_id = result[0]
                    else:
                        # Insert the job location into the job locations table
                        c.execute('INSERT INTO job_locations (location) VALUES (?)', (job_location,))
                        job_location_id = c.lastrowid
                except KeyError:
                    job_location = None
                    job_location_id = None
                    
                try:
                    snippet = job['snippet']
                except KeyError:
                    snippet = None
                    
                try:
                    salary = job['salary']
                    if "hour" in salary:
                        # Extract the two numbers from the string
                        numbers = [float(s) for s in re.findall(r'\d+\.*\d*', salary)]
                        # Calculate the average hourly rate
                        hourly_rate = sum(numbers) / len(numbers)
                        # Calculate the annual salary
                        annual_salary = hourly_rate * 2080
                    elif "day" in salary:
                        # Extract the two numbers from the string
                        numbers = [float(s) for s in re.findall(r'\d+\.*\d*', salary)]
                        # Calculate the average daily rate
                        daily_rate = sum(numbers) / len(numbers)
                        # Calculate the annual salary
                        annual_salary = daily_rate * 260
                    else:
                        # Extract the one or two numbers from the string
                        numbers = [float(s[:-1]) * 1000 if s[-1] == "k" else float(s) for s in re.findall(r'\d+\.*\d*\w*', salary)]
                        # Calculate the average annual salary
                        if len(numbers) == 1:
                            annual_salary = numbers[0]
                        else:
                            annual_salary = sum(numbers) / len(numbers)
        
                except KeyError:
                    salary = None
                    
                try:
                    company = job['company']
                except KeyError:
                    company = None

                c.execute('INSERT OR IGNORE INTO jobs (title, major_id, job_location_id, snippet, salary, company) SELECT ?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title=? AND company=?)', (title, major_id, job_location_id, snippet, annual_salary, company, title, company))
                if c.rowcount >= 1:
                    counter += 1
            # Commit the changes and close the connection
            conn.commit()
            
            conn.close()

def companyList():
    import sqlite3
    # Open a connection to the database
    conn = sqlite3.connect('database.db')

    # Get a cursor object for the database connection
    cursor = conn.cursor()

    # Define a SQL query to select all unique company names from the jobs table
    sql_query = '''
    SELECT DISTINCT company
    FROM jobs
    '''

    # Execute the SQL query and fetch all the results into a list
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Extract the company names from the results and store them in a list
    company_names = [row[0] for row in results]
    
    #print(company_names)

    # Close the database connection
    conn.close()
    return company_names




def get_ticker(company_name):
    import requests
    from bs4 import BeautifulSoup

    # Define Yahoo Finance search URL
    YAHOO_FINANCE_URL = f"https://finance.yahoo.com/lookup?s={company_name}"

    # Send the search request
    response = requests.get(YAHOO_FINANCE_URL)

    # Check if the response is valid
    if response.status_code == 200:
        try:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the first search result
            result = soup.find("td", {"class": "data-col0 Ta(start) Pstart(6px)"})

            # Check if a result was found
            if result is not None:
                # Extract the ticker symbol from the result
                ticker = result.text.strip()
                return ticker
            else:
                print(f"No ticker found for '{company_name}'")
                return None
        except Exception as e:
            print(f"Failed to parse HTML response: {e}")
            return None
    else:
        print(f"Failed to get ticker for '{company_name}'. Status code: {response.status_code}")
        return None

def get_price_history(company_names):
    import requests
    import sqlite3
    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stocks
                (date TEXT, open REAL, high REAL, low REAL, close REAL, volume INTEGER, company TEXT)''')
    counter = 0
    # Loop through the list of company names
    for company_name in company_names:
        if counter >= 25:
            break
        ticker = get_ticker(company_name)
        if ticker is None:
            # If no ticker found, skip to the next company
            continue
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(url)
        try:
            data = response.json()['Time Series (Daily)']
        except:
            print("Failed to load JSON, please try again in a few minutes, you've reached a limit")
            return None

        for date, values in data.items():
            if counter >= 25:
                break
            # Retrieve the stock ticker from the JSON response

            # Check if data with the same date and company has already been inserted into the database
            c.execute("SELECT * FROM stocks WHERE date = ? AND company = ?", (date, company_name))
            rows = c.fetchall()
            if len(rows) > 0:
                continue

            # Insert the data into the "stocks" table
            open_price = values['1. open']
            high_price = values['2. high']
            low_price = values['3. low']
            close_price = values['4. close']
            volume = values['6. volume']
            company = company_name
            c.execute("INSERT INTO stocks (date, open, high, low, close, volume, company) VALUES (?, ?, ?, ?, ?, ?, ?)", (date, open_price, high_price, low_price, close_price, volume, company_name))
            counter += 1

        if counter == 0:
            print(f"No new data added for {company_name}")
        else:
            print(f"Added {counter} new data points for {company_name}")

    conn.commit()
    conn.close()

def plotStocks():
    import sqlite3
    import pandas as pd
    import matplotlib.pyplot as plt

    # Connect to the SQL database
    conn = sqlite3.connect('database.db')

    # Retrieve data from the SQL table
    df = pd.read_sql_query('SELECT date, close, company FROM stocks', conn)

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Get unique companies
    unique_companies = df['company'].unique()

    # Plot a separate line for each unique company
    for company in unique_companies:
        company_df = df[df['company'] == company]
        plt.plot(company_df['date'], company_df['close'], label=company)

    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Close Price Over Time by Company')
    plt.legend()
    plt.show()


#This whole process works a lot better and is a lot more useful when you remove the 25 row limits (if/break statements)

#atlasMajor('Information BS')
#atlasMajor('Information BS')
#atlasMajor('Communication BA')
#atlasMajor('Communication BA')
#atlasMajor()
#atlasMajor()

#convertGrades()
#majorAvg('median_grade')
#salary(GPTsalary('Information BS'))
#salary(GPTsalary('Communication BA'))
#salary(GPTsalary('Computer Engineering BSE'))
get_price_history(companyList())
#plotStocks()