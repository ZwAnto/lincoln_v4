### NAVIGATOR
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

import numpy as np

class chrome:
    def __init__(self):
        
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--incognito')
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.option.set_capability("pageLoadStrategy", "normal");
        
        self.driver = webdriver.Chrome(executable_path="/opt/chromedriver", options=self.option)
        
    def reset(self):
        self.driver = webdriver.Chrome(executable_path="/opt/chromedriver", options=self.option)