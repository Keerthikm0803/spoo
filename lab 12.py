from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Perform a Google search and return results
def google_search(driver, query):
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(query)
    search_box.submit()
    
    # Wait for search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
    )
    
    # Extract the search result titles and links
    results = []
    for result in driver.find_elements(By.CSS_SELECTOR, "h3"):
        title = result.text
        link = result.find_element(By.XPATH, "..").get_attribute("href")
        results.append((title, link))
    
    return results

# Navigate to the first search result
def open_first_result(driver, results):
    if results:
        driver.get(results[0][1])
        time.sleep(5)  # Let the page load

# Example usage
if __name__== "__main__":
    driver = setup_driver()
    try:
        query = "Selenium Python tutorial"
        results = google_search(driver, query)
        for title, link in results[:5]:  # Display the first 5 results
            print(f"Title: {title}\nLink: {link}\n")
        open_first_result(driver, results)
    finally:
        driver.quit()