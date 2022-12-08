from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
class SignUp:
    def __init__(self):
        self.name1="author 1"
        self.name2="author 2"
        self.password="12345678"
        self.github1="https://github.com/em1i"
        self.github2="https://github.com/happycat33"
        self.website1 = 'https://superlative-gelato-dcf1b6.netlify.app/login'
        self.website2 = "http://localhost:3000"
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(self.website1) 


    def Author1(self ):
        """
        Test user register
        """
        try:

            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="signup-button"]'))))
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="reg-login"]'))
            time.sleep(1)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/form/div[2]/input')
            keyword.send_keys(self.name1)
            time.sleep(2)
            keyword =self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/form/div[3]/input')
            keyword.send_keys(self.password)
            time.sleep(2)
            keyword =self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/form/div[4]/input')
            keyword.send_keys(self.password)
            time.sleep(2)
            keyword =self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/form/div[5]/input')
            keyword.send_keys(self.github1)
            time.sleep(2)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="submit-button"]')
            keyword.click()
            time.sleep(1)
            text =self.driver.find_element(By.XPATH,'//*[@id="submit-button"]')
            text.click()
            time.sleep(2)
            self.driver.back()
            print("*"*30)
            print("author 1 register test finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 register:\n")
            print(e)
           
    def Author2(self):
        """
        Test user register
        """
        try:
            self.driver.get(self.website1) 
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="signup-button"]'))))
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="reg-login"]'))
            
            time.sleep(1)
            keyword =self.driver.find_element(By.XPATH, "//*[@id='root']/div[2]/div[2]/form/div[2]/input")
            keyword.send_keys(self.name2)
            keyword =self.driver.find_element(By.XPATH,"//*[@id='root']/div[2]/div[2]/form/div[3]/input")
            keyword.send_keys(self.password)
            keyword =self.driver.find_element(By.XPATH,"//*[@id='root']/div[2]/div[2]/form/div[4]/input")
            keyword.send_keys(self.password)
            keyword =self.driver.find_element(By.XPATH,"//*[@id='root']/div[2]/div[2]/form/div[5]/input")
            keyword.send_keys(self.github2)
            keyword =self.driver.find_element(By.XPATH, "//*[@id='submit-button']")
            keyword.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(1)
            print("*"*30)
            print("author 2 register test finished!")
            print("*"*30)
        except Exception as e:
            print("Error happened in author 2 register:\n")
            print(e)
            
        
    
"""
Test user register
"""
signup = SignUp()
# Test first user register, for later use
signup.Author1()
# Test second user register, for later use
signup.Author2()
signup.driver.quit()













