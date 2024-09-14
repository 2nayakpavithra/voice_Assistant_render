from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MusicPlayer:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.playing = False  # Flag to track if music is currently playing

    def play(self, query):
        try:
            self.driver.get('https://www.youtube.com')

            # Wait until the search box is visible
            search_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#search'))
            )

            # Input the query into the search box
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            # Wait until the video results are visible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-video-renderer'))
            )

            # Click on the first video result
            first_video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-video-renderer ytd-thumbnail'))
            )
            first_video.click()

            self.playing = True  # Set playing flag to True

        except Exception as e:
            print(f"Exception occurred: {e}")
            self.playing = False  # Ensure playing flag is False on error

    def is_playing(self):
        return self.playing

    def stop(self):
        self.driver.quit()
        self.playing = False
