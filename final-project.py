#Step 1, get classes required from audit
#Step 2, search for classes that fit criteria, add to DB
#Step 3, find score for each teach for each top class in class DB

#Step 2, Atlast:
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
        print(title, median_grade, desire, understanding, workload, expectation, interest,'\n\n')

    # Connect to the database
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+'classes.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Create the table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes
            (id INTEGER PRIMARY KEY, title TEXT, median_grade INTEGER, workload INTEGER, understanding INTEGER, desire INTEGER, expectation INTEGER)
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


#we can use LSA course guide to get a list of classes that fall under certain criteria. Example:
'''
Can use https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=f_23_2460&cgtype=ug&show=20&dist=NS to find classes in F_23_24 that are
NS credits. Can change any variables to alter. For example, increase "show" to 40 to show more.
'''
getClassAtlas(['https://atlas.ai.umich.edu/course/SI%20206/', 'https://atlas.ai.umich.edu/course/IHS%20340/', 'https://atlas.ai.umich.edu/course/STATS%20250/'])