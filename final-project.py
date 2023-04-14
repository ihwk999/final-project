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
                    major = None
                    major = None

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
                    major = None
                    major = None

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
    return output



def salary(jobLst):
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
    for jobM in jobLst:
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
            c.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, job_location_id INTEGER, snippet TEXT, salary TEXT, company TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS job_locations (id INTEGER PRIMARY KEY, location TEXT)')
            # Loop through the jobs and insert them into the database
            for job in json_data['jobs']:
                if counter >= 25:
                    break
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

                c.execute('INSERT OR IGNORE INTO jobs (title, job_location_id, snippet, salary, company) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title=? AND company=?)', (title, job_location_id, snippet, annual_salary, company, title, company))
                if c.rowcount >= 1:
                    counter += 1
            # Commit the changes and close the connection
            conn.commit()
            
            conn.close()

def get_price_history(symbol):
    import requests

    ALPHA_VANTAGE_API_KEY = 'KUGOCCJRWJ0PQBI1'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()['Time Series (Daily)']
    price_history = []
    for date, values in data.items():
        price_history.append({'date': date, 'open': values['1. open'], 'high': values['2. high'], 'low': values['3. low'], 'close': values['4. close'], 'volume': values['6. volume']})
    return price_history
atlasMajor()
#salary(GPTsalary())