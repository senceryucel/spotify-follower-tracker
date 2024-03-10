from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class FetchFollowers:
    def __init__(self, user_id):
        self.URL = f"https://open.spotify.com/user/{user_id}/followers"
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        self.followers_list = []
        self.init_followers()


    def init_followers(self):
        """
        Initializes the followers list
        """
        self.driver.get(self.URL)
        self.followers_list = self.get_followers()


    def get_followers(self):
        """
        Returns the followers list
        """
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        followers = []
        for follower in self.driver.find_elements(By.XPATH, "//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/section/div[2]/div"):
            followers.append(follower.text.split("\n")[0])
        return followers
    

    def compare_followers(self):
        """
        Compares the followers list
        """
        all_followers = self.get_followers()
        new_followers = [follower for follower in all_followers if follower not in self.followers_list]
        lost_followers = [follower for follower in self.followers_list if follower not in all_followers]
        self.followers_list = all_followers
        return new_followers, lost_followers