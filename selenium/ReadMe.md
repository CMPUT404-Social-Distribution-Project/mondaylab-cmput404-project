# To start test
 - Prerequest: you should install Chrome in your Windows or Ubuntu environment
 - self.website2 and self.website1 are different, one is run locally, one is run deployed.
 - ## test remote

	>  step 0: pip install selenium && pip install webdriver-manager
	> step 1: run signup.py first, then run login.py

 - ## test local
   > step 0: npm install && pip install selenium && pip install webdriver-manager
   > step 1: frontend is running in heroku
   > step 2: backend is running in heroku
   > step 3: change from self.website1 to self.website2 in the self.driver.get(self.website1)--line 24
   > step 4: run signup.py first, then run login.py

---
# signup.py
  - register user for later use

---
# Login.py
- login two user
- create public post
- create markdown post
- create firend post
- edit profile
- send follow request and accept follow request
- send comment
- like post