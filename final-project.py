#Step 1, get classes required from audit
#Step 2, search for classes that fit criteria, add to DB
#Step 3, find score for each teach for each top class in class DB

#Step 2, Atlast:
def getClassAtlas(class_url='https://atlas.ai.umich.edu/course/SI%20206/'):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup

    # Set the path to your ChromeDriver executable
    chromedriver_path = r"C:\Users\gecko\Downloads\chromedriver_win32 (4)\chromedriver.exe"

    # Initialize a Chrome webdriver instance
    driver = webdriver.Chrome(chromedriver_path)

    # Navigate to the website
    driver.get(class_url)

    # Wait for the user to log in
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "myNavbar"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print(soup.prettify())
    #this now waits to continue until the NavBar id is shown. Essentially, it waits until the user is logged in to continue.
    
    finally:
        driver.quit()


#we can use LSA course guide to get a list of classes that fall under certain criteria. Example:
'''
Can use https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=f_23_2460&cgtype=ug&show=20&dist=NS to find classes in F_23_24 that are
NS credits. Can change any variables to alter. For example, increase "show" to 40 to show more.
'''