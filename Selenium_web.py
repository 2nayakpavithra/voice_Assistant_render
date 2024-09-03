from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class infow:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_info(self, query):
        self.query = query
        self.driver.get('https://www.wikipedia.org')

        try:
            search = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInput"]'))
            )

            search.click()
            search.send_keys(query)

            enter = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-form"]/fieldset/button'))
            )
            enter.click()

            # Wait for the article content to load
            article_content = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[2]'))
            )

            info_text = article_content.text.split('\n')[:2]
            self.info_text = ' '.join(info_text)

        except Exception as e:
            print(f"Exception occurred: {e}")

        return self.info_text

    def close_driver(self):
        self.driver.quit()
