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

    # Set the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\gecko\Downloads\chromedriver_win32 (4)\chromedriver.exe"

    # Initialize a Chrome webdriver instance
    driver = webdriver.Chrome(chromedriver_path)

    # Navigate to the website
    for url in class_url:
        driver.get(url)

        # Wait for the user to log in
        
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "myNavbar"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the span element with class 'bold blue-highlight-text'
        median_grade_span = soup.find('span', class_='bold blue-highlight-text')
        median_grade = median_grade_span.text
        print(median_grade)


        title_element = soup.find('title')
        title = title_element.text
        print(title)
        
        element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course-eval-card-container"))
        )
        
        print('hi')

        elements = driver.find_elements_by_class_name("course-eval-card-container")
        print(elements[1].text)
    count = 0
    for element in elements:
        if  count == 0:
            desire = element.text #YOU LEFT OFF RIGHT HERE, NEED TO EXTRACT %s
            count += 1
        elif count == 1:
            understanding = element.text
            count += 1
        elif count == 2:
            workload = element.text
            count += 1
        elif count == 3:
            expectation = element.text
            count += 1
        elif count == 4:
            interest = element.text
    print(desire, understanding, workload, expectation, interest)

    # Connect to the database
    conn = sqlite3.connect('classes.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes
        (id INTEGER PRIMARY KEY, median_grade TEXT, title TEXT, workload TEXT, understanding TEXT, desire TEXT, expectations TEXT)
        ''')
    cursor.execute('''
        INSERT OR IGNORE INTO classes (median_grade, title, workload, understanding, desire, expectations)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (median_grade, title, workload, understanding, desire, expectations))
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
getClassAtlas()