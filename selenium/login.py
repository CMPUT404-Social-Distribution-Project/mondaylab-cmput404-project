from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
class Login:
    def __init__(self):
        self.name1="author 1"
        self.name2="author 2"
        self.password="12345678"
        self.github1="https://github.com/em1i"
        self.github2="https://github.com/happycat33"
        self.website1 = 'https://superlative-gelato-dcf1b6.netlify.app'
        self.website2 = "http://localhost:3000"
        self.image="https://cdn2.momjunction.com/wp-content/uploads/2021/10/148-Funny-Last-Names-Or-Surnames-From-Across-The-World.jpg"
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(self.website1) 


    def Author1(self ):
        """
        User first to login, then check if homepage render correctly
        """
        try:
            self.driver.get(self.website1+'/login')
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))))
            time.sleep(1)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/form/div[1]/input')
            keyword.send_keys(self.name1)
            keyword =self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/form/div[2]/input')
            keyword.send_keys(self.password)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="submit-button"]')
            keyword.click()
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("Author login finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 login:\n")
            print(e)
    def Author1_create_post(self ):
        """
        After login, then click the create post icon, to create a post
        The post for later use 
        """
        try:

            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            # ///*[@id="sidebar"]/li[1]/div
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[1]/div'))))
            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[2]/div[1]/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[1]/input'))
            elem.send_keys("This is first test post ")
            # /html/body/div[3]/div/div/form/div[2]/div[2]/textarea
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[2]/textarea'))
            elem.send_keys("This is first test post made by author 1")

            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[3]/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button'))))
            time.sleep(3)
            #self.driver.back()
            print("*"*30)
            print("Create post test finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 creat post:\n")
            print(e)
    def Author1_create_friend_post(self ):
        """
        After login, then click the create post icon, to create a friend post
        The post for later use 
        """
        try:

            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            # ///*[@id="sidebar"]/li[1]/div
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[1]/div'))))
            time.sleep(1)
            # User send friend post
            # /html/body/div[3]/div/div/form/div[1]/div/button[2]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[1]/div/button[2]'))))

            # /html/body/div[3]/div/div/form/div[2]/div[1]/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[1]/input'))
            elem.send_keys("This is friend test post ")
            # /html/body/div[3]/div/div/form/div[2]/div[2]/textarea
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[2]/textarea'))
            elem.send_keys("This is friend test post made by author 1, this post should go to author 2's inbox")

            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[3]/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button'))))
            time.sleep(3)
            #self.driver.back()
            print("*"*30)
            print("Create friend post test finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 creat friend post:\n")
            print(e)
    def Author1_create_markdown_post(self ):
        """
        After login, then click the create post icon, to create a markdown format post
        """
        try:

            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            # ///*[@id="sidebar"]/li[1]/div
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[1]/div'))))
            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[2]/div[1]/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[1]/input'))
            elem.send_keys("This is markdown test post ")
            # /html/body/div[3]/div/div/form/div[2]/div[2]/textarea
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[2]/textarea'))
            elem.send_keys("# This is markdown test post made by author 1")

            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[3]/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button'))))
            time.sleep(3)
            #self.driver.back()
            print("*"*30)
            print("Create markdown post test finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 creat markdown post:\n")
            print(e)       
    def Author2(self):
        """
        User first to login, then check if homepage render correctly
        """
        try:
            self.driver.get(self.website1+'/login')
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))))
            time.sleep(1)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/form/div[1]/input')
            keyword.send_keys(self.name2)
            keyword =self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/form/div[2]/input')
            keyword.send_keys(self.password)
            keyword =self.driver.find_element(By.XPATH, '//*[@id="submit-button"]')
            keyword.click()
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("author 2 login finished!")
            print("*"*30)
        except Exception as e:
            print("Error happened in author 2 login:\n")
            print(e)

    def Author2_create_post(self):
        """
        After login, then click the create post icon, to create a post
        The post for later use 
        """
        try:
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            # ///*[@id="sidebar"]/li[1]/div
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[1]/div'))))
            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[2]/div[1]/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[1]/input'))
            elem.send_keys("This is second test post ")
            # /html/body/div[3]/div/div/form/div[2]/div[2]/textarea
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[2]/textarea'))
            elem.send_keys("This is second test post made by author 2")

            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[3]/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button'))))
            time.sleep(3)
            self.driver.back()
            print("*"*30)
            print("Create post test finished!")
            print("*"*30)
        except Exception as e:
            print("Error happened in author 2 create post:\n")
            print(e)
    def clickNavBar(self):
        """
        User to test each icon in sidebar is clickable.
        User test if github activity page display
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[2]/div'))))
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1')) 
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[4]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1
            # Test if go to local explore page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1'))  
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[5]/div'))))
            # //*[@id="root"]/div[2]/div/div/div/div/h5
            # Test if go to remote explore page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div/h5'))    
            time.sleep(15)
            self.driver.get(f'{self.website1}/stream/github')
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("Click nav bar test finished!")
            print("*"*30)
        except Exception as e:
            print("Error happened in author 2 register:\n")
            print(e)
            
    def See_author1_post(self):
        """
        User current user can see other's public post.
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[4]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1
            # Test if go to local explore page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1'))  
            # Test if author1's post display
            self.driver.find_elements(By.XPATH, "//*[contains(text(), 'author 1')]")
            assert("author 1" in self.driver.page_source)
            time.sleep(2)
            self.driver.back()
            print("*"*30)
            print("User can see other's post test finished!")
            print("*"*30)
        except Exception as e:
            print("Error happened when see other's post:\n")
            print(e)

    def author2_follow_author1(self):
        """
        Current user can follow other user
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[4]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1
            # Test if go to local explore page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1'))  
            # Test if author1's post display
            # elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
            #     "//*[contains(text(), 'author 1')]")) 
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'author 1')]"))))
            # Test if go to user's profile
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'author 1')]")) 
            # Click follow button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="followButton"]'))))
            # Test if follow request send successfully
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'Sent')]")) 

            assert("author 1" in self.driver.page_source)
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("User can send follow request to others!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user send follow request:\n")
            print(e)
    def edit_profile(self):
        """
        User can edit their profile
        """
        try:
            time.sleep(1)
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/nav/div/div/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/div[2]/div[3]/button
            # Test if go to user's profile
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'author')]")) 
            # Test edit button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div[1]/div[2]/div[3]/button'))))
            # edit image
            # /html/body/div[3]/div/div/div[2]/form/div/div[1]/input
            # https://cdn2.momjunction.com/wp-content/uploads/2021/10/148-Funny-Last-Names-Or-Surnames-From-Across-The-World.jpg
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "/html/body/div[3]/div/div/div[2]/form/div/div[1]/input"))
            elem.clear()
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/div[2]/form/div/div[1]/input'))
            elem.send_keys(self.image)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))))

            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("User can edit profile image!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user edit profile:\n")
            print(e)


    def author1_accept_follow_request_in_inbox(self):
        """
        Current user can see folllow request from others in inbox.
        Current user can accept follow request
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            # Test if follow request button clickable
            # //*[@id="left-tabs-example-tab-follow"]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-follow"]'))))
            time.sleep(1)
            # Now, follow request tab should not be empty
            assert("No follow request" not in self.driver.page_source)
            # Author2's name should display
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'author 2')]")) 
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Accept')]"))))
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-follow"]'))))
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("User can accept follow request!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user accept follow request:\n")
            print(e)
    def author2_see_friend_post_in_inbox(self):
        """
        The friend post created by author 1, 
        the post only display in author2's inbox (since author 2 follow author 1), 
        it will not show in explore public page
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            # Test if post button clickable
            # //*[@id="left-tabs-example-tab-post"]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-post"]'))))
            time.sleep(1)
            # Now, follow request tab should not be empty
            assert("No post" not in self.driver.page_source)
            # Author1's name should display, frined post should display
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'friend')]")) 
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[4]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1
            # Test if go to local explore page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/div[1]/h1'))  
            # Test if author1's post display, author1's friend post should not display
            assert("This is friend test post" not in self.driver.page_source)
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("User can see friend post! User cannot see friend post in explore public page!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user see friend post:\n")
            print(e)
    def Author2_comment_post(self):
        """
        User can comment post
        """
        try:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[3]/svg[1]
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            assert("This is friend test post" in self.driver.page_source)
            # send comment
            # //*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[5]/form/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[5]/form/input'))
            elem.send_keys("This is first comment from author 2")
            # //*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[5]/form/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[5]/form/button'))))
            time.sleep(2)
            print("*"*30)
            print("User can comment friend post!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user comment friend post:\n")
            print(e)
    def Author2_like_post(self):
        """
        User can like post
        """
        try:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="left-tabs-example-tabpane-post"]/div/div[2]/div[3]/svg[1]
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            assert("This is friend test post" in self.driver.page_source)
            # send like
            # //*[@id="root"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/svg[3]/path[2]
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@class="like-icon"]'))
            elem.click()
            time.sleep(2)
            print("*"*30)
            print("User can like friend post!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user like friend post:\n")
            print(e)

    def author1_see_commnet_like_in_inbox(self):
        """
        The friend post created by author 1, 
        the commnet/like from author 2
        the comment/like should display in author1's inbox
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            # Test if comment button clickable
            # //*[@id="left-tabs-example-tab-comment"]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-comment"]'))))
            time.sleep(1)
            # Now, comment tab should not be empty
            assert("No comments" not in self.driver.page_source)
            # Author2's name should display, comment should display
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'author 2')]")) 
            time.sleep(1)
            # Test if author2's comment display
            assert("This is first comment from author 2" in self.driver.page_source)
            time.sleep(2)
            # Test if like button clickable
            # //*[@id="left-tabs-example-tab-like"]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-like"]'))))
            time.sleep(1)
            # Now, like tab should not be empty
            assert("No like" not in self.driver.page_source)
            # Author2's name should display, comment should display
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'author 2')]")) 
            time.sleep(1)
            # Test if author2's comment display
            assert("liked your post" in self.driver.page_source)
            #self.driver.back()
            print("*"*30)
            print("User can see comment and like!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user see comment and like:\n")
            print(e)

    def share(self):
        """
        After login, share the post to author 2
        """
        try:

            time.sleep(1)
            # Test if go to my feed page
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))
            time.sleep(2)
            # ///*[@id="sidebar"]/li[1]/div
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[1]/div'))))
            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[2]/div[1]/input
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[1]/input'))
            elem.send_keys("This is share test post ")
            # /html/body/div[3]/div/div/form/div[2]/div[2]/textarea
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '/html/body/div[3]/div/div/form/div[2]/div[2]/textarea'))
            elem.send_keys("This is share test post made by author 1")

            time.sleep(1)
            # /html/body/div[3]/div/div/form/div[3]/button
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/svg[3]/path[2]
            elem = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,
                '//*[@class="share-icon"]'))
            elem.click()

            #self.driver.back()
            print("*"*30)
            print("Share post test finished!")
            print("*"*30)
            
        except Exception as e:
            print("Error happened in author 1 share post:\n")
            print(e)

    def Author2_see_share_post_from_autho1(self):
        """
        Author 1 share a post, thi spost will go to author2's inbox.
        Author 2 now check if this post display in inbox
        """
        try:
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sidebar"]/li[3]/div'))))
            time.sleep(1)
            # //*[@id="root"]/div[2]/div/div/div/div[1]/h1
            # Test if go to inbox page
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
                '//*[@id="root"]/div[2]/div/div/div/div[1]/h1'))  
            # Test if post button clickable
            # //*[@id="left-tabs-example-tab-post"]
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="left-tabs-example-tab-post"]'))))
            time.sleep(1)
            # Now, post tab should not be empty
            assert("No post" not in self.driver.page_source)
            # Author1's name should display, shared post should display
            elem = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.XPATH,
             "//*[contains(text(), 'share test post')]")) 
            time.sleep(2)
            #self.driver.back()
            print("*"*30)
            print("User can see friend post! User cannot see friend post in explore public page!")
            print("*"*30)
        except Exception as e:
            print("Error happened when user see friend post:\n")
            print(e)




"""
Start test:
Test create public post
Test sidebar render correctly
"""
login = Login()
#Test user 1 login and create public post.
login.Author1()
login.Author1_create_post()
login.Author1_create_markdown_post()

#Test user 2 login and create public post.
login.Author2()
login.Author2_create_post()

#Test siderbar if render correctly.
login.clickNavBar()

#Test if user2 can see user1's post
login.See_author1_post()

#Test user 2 can follow use 1
login.author2_follow_author1()

#Test if user 1 can see follow request in inbox
login.Author1()
login.author1_accept_follow_request_in_inbox()

#Test if user 2 can see friendly post from user 1
login.Author1()
login.Author1_create_friend_post()
login.Author2()
login.author2_see_friend_post_in_inbox()

# Test author 2 commnet authoor1's post
login.Author2()
login.Author2_comment_post()
# Test author 2 like authoor1's post
login.Author2()
login.Author2_like_post()

# test Author 1 can see comment and like from author 2
login.Author1()
login.author1_see_commnet_like_in_inbox()

#Test user 1 login and create markdown public post.
login.Author1()
login.Author1_create_markdown_post()

#Test share, author 1 share post, author 2 see shared post in inbox
login.Author1()
login.share()
login.Author2()
login.Author2_see_share_post_from_autho1()


# Test user edit profile
login.Author1()
login.edit_profile()

#Close the window
login.driver.quit()













