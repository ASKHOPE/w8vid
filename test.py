import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

# driver = webdriver.Firefox()
# driver.get('https://the-internet.herokuapp.com/login')

# driver.find_element(By.ID, 'username').send_keys("tomsmith")
# driver.find_element(By.ID, 'password').send_keys("SuperSecretPassword!")
# driver.find_element(By.CLASS_NAME, "radius").click()
# driver.find_element(By.CLASS_NAME, "button secondary radius").click()


class HeroKuapp(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()


    def test_login(self):
        #verify succesful login
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/login')

        driver.find_element(By.ID, 'username').send_keys("tomsmith")
        driver.find_element(By.ID, 'password').send_keys("SuperSecretPassword!")
        driver.find_element(By.CLASS_NAME, "radius").click()
        x = driver.find_element(By.ID, "flash").text

        self.assertIn("logged into", x)

    def test_fail_login_userName(self):
        #verify wrong username
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/login')

        driver.find_element(By.ID, 'username').send_keys("x")
        driver.find_element(By.ID, 'password').send_keys("SuperSecretPassword!")
        driver.find_element(By.CLASS_NAME, "radius").click()

        x = driver.find_element(By.ID, "flash").text
        self.assertIn("username is invalid", x)

    def test_fail_login_password(self):
        #verify failed password
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/login')

        driver.find_element(By.ID, 'username').send_keys("tomsmith")
        driver.find_element(By.ID, 'password').send_keys("x!")
        driver.find_element(By.CLASS_NAME, "radius").click()

        x = driver.find_element(By.ID, "flash").text
        self.assertIn("password is invalid", x)

    def test_logOut(self):
        #verify logout button
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/login')

        driver.find_element(By.ID, 'username').send_keys("tomsmith")
        driver.find_element(By.ID, 'password').send_keys("SuperSecretPassword!")
        driver.find_element(By.CLASS_NAME, "radius").click()
        #sleep(5)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Logout").click()
        x = driver.find_element(By.ID, "flash").text
        self.assertIn("logged out", x)

    def test_slider(self):
        #verify slider function
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/horizontal_slider')
        driver.find_element(By.XPATH, "/html[@class='no-js']/body/div[@class='row'][2]/div[@id='content']/div[@class='example']/div[@class='sliderContainer']/input").send_keys(Keys.RIGHT)
        x = driver.find_element(By.ID, "range").text
        self.assertIn("0.5", x)

    def test_dropdown_once(self):
        #verify page will select first option
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/dropdown')
        x = driver.find_element(By.ID, "dropdown")
        x.send_keys(Keys.DOWN)
        self.assertIn("Option 1", x.text)

    def test_dropdown_twice(self):
        #verify page will allow second option in drop down
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/dropdown')
        x = driver.find_element(By.ID, "dropdown")
        x.send_keys(Keys.DOWN)
        x.send_keys(Keys.DOWN)
        self.assertIn("Option 2", x.text)

    def test_dropdown_down_up(self):
        #verify page will change selected option after reaching bottom
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/dropdown')
        x = driver.find_element(By.ID, "dropdown")
        x.send_keys(Keys.DOWN)
        x.send_keys(Keys.UP)
        self.assertIn("Option 1", x.text)       

    def test_redirect(self):
        #verify page will folow link
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/redirector')
        driver.find_element(By.ID, "redirect").click()
        self.assertIn( 'status code', driver.page_source.lower())
    
    def test_keypress(self):
        #verify page displays key press
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/key_presses')
        driver.find_element(By.XPATH, "/html[@class='no-js']/body/div[@class='row'][2]/div[@id='content']/div[@class='example']/form/input[@id='target']").send_keys(Keys.BACKSPACE)
        x = driver.find_element(By.ID, "result").text
        self.assertIn("BACK_SPACE", x)

    def test_second_keypress(self):
        #verify that the page displays second key press
        driver = self.driver
        driver.get('https://the-internet.herokuapp.com/key_presses')
        driver.find_element(By.XPATH, "/html[@class='no-js']/body/div[@class='row'][2]/div[@id='content']/div[@class='example']/form/input[@id='target']").send_keys(Keys.BACKSPACE)
        driver.find_element(By.XPATH, "/html[@class='no-js']/body/div[@class='row'][2]/div[@id='content']/div[@class='example']/form/input[@id='target']").send_keys(Keys.INSERT)
        x = driver.find_element(By.ID, "result").text
        self.assertIn("INSERT", x)

    def test_context(self):
        #would not pass without the driver being a fresh driver. unclear what the difference would be but it works as intended.
        driver = webdriver.Firefox()
        action = ActionChains(driver)
        driver.get('https://the-internet.herokuapp.com/context_menu')
        sleep(4)
        box = driver.find_element(By.ID, "hot-spot")
        action.context_click(box).perform()
        alert = driver.switch_to.alert
        self.assertIn("selected", alert.text)
        driver.close()

    def tearDown(self) -> None:
        self.driver.close()

unittest.main()