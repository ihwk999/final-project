#Step 1, get classes required from audit
#Step 2, search for classes that fit criteria, add to DB
#Step 3, find score for each teach for each top class in class DB

#Step 2, Atlast:
def atlasMajor(major= "Information BS"):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import sqlite3
    import re
    import os
    major = major.replace(' ','%20')
    url = 'https://atlas.ai.umich.edu/major/'+major
    # Set the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\gecko\Downloads\chromedriver_win32 (4)\chromedriver.exe"

    # Initialize a Chrome webdriver instance
    driver = webdriver.Chrome(chromedriver_path)


    driver.get(url)

    element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "myNavbar"))
        )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    course_container = soup.find('div', class_ = 'common-courses-container')
    course = course_container.text
    links = []
    for link in course_container.find_all('a'):
        links.append(link.get('href'))
    links = [x for x in links if x is not None and '/bookmark/' not in x]
    print(links)
    return(links)
    
    


def getClassAtlas(class_url=['https://atlas.ai.umich.edu/course/SI%20206/']):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    import sqlite3
    import re
    import os

    # Set the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\gecko\Downloads\chromedriver_win32 (4)\chromedriver.exe"

    # Initialize a Chrome webdriver instance
    driver = webdriver.Chrome(chromedriver_path)

    # Navigate to the website
    for url in class_url:
        driver.get(url)

        # Wait for the user to log in
        
        element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "myNavbar"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the span element with class 'bold blue-highlight-text'
        median_grade_span = soup.find('span', class_='bold blue-highlight-text')
        median_grade = median_grade_span.text


        title_element = soup.find('title')
        title = title_element.text
        
        element = WebDriverWait(driver, 30).until(
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
        print('\n',title, median_grade, desire, understanding, workload, expectation, interest)

    # Connect to the database
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+'classes.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Create the table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes
            (id INTEGER PRIMARY KEY, title TEXT, median_grade TEXT, workload INTEGER, understanding INTEGER, desire INTEGER, expectation INTEGER)
            ''')
        cursor.execute('''
            INSERT OR IGNORE INTO classes (title, median_grade, workload, understanding, desire, expectation)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, median_grade, workload, understanding, desire, expectation))
        conn.commit()

        cursor.close()
        conn.close()
            
            
            
        #this now waits to continue until the NavBar id is shown. Essentially, it waits until the user is logged in to continue.
        
    
    driver.quit()

def GPTsalary(major = 'Information BS'):
    import openai
    import re
    openai.api_key = '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'

    # Set the prompt for the OpenAI API
    prompt = ("according to Payscale.com, what is the average annual salary in usd of an individual who majaored in " + major + " in college")

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

    print(message)

    pattern = r"\$\d{1,4}(,\d{3})*"
    salary_match = re.search(pattern, message)

# Check if a match was found and print the result
    if salary_match:
        print("Salary found:", salary_match.group(0))
        return(salary_match.group(0))
    else:
        print("Salary not found in the text.")

    # Print the generated message
    

def salary(major):
    import http.client
    import sqlite3
    import json

    host = 'jooble.org'
    key = '5d5716ba-8dec-4784-b885-926a7ebee49f'

    connection = http.client.HTTPConnection(host)
    #request headers
    headers = {"Content-type": "application/json"}
    #json query
    for x in range(4):
        body = '{ "keywords": "'+major+'", "location": "US", "page": '+str(x)+' }' #this limit isint working
        connection.request('POST','/api/' + key, body, headers)
        response = connection.getresponse()
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        #print(json_data)

        conn = sqlite3.connect('salaries.db')
        c = conn.cursor()
        # Create the table if it doesn't already exist
        c.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, location TEXT, snippet TEXT, salary TEXT, company TEXT)')

        # Loop through the jobs and insert them into the database
        for job in json_data['jobs']:
            title = job['title']
            location = job['location']
            snippet = job['snippet']
            salary = job['salary']
            company = job['company']
            c.execute('INSERT OR IGNORE INTO jobs (title, location, snippet, salary, company) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title=?)', (title, location, snippet, salary, company, title))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


#we can use LSA course guide to get a list of classes that fall under certain criteria. Example:
'''
Can use https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=f_23_2460&cgtype=ug&show=20&dist=NS to find classes in F_23_24 that are
NS credits. Can change any variables to alter. For example, increase "show" to 40 to show more.
'''
#getClassAtlas(['https://atlas.ai.umich.edu/course/SI%20206/', 'https://atlas.ai.umich.edu/course/IHS%20340/', 'https://atlas.ai.umich.edu/course/STATS%20250/'])
salary('BioTech')