from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from server import app


def test_logout():
    if app.testing:
        print(app.testing)
        service = Service("tests/fonctionnels/chromedriver")
        driver = webdriver.Chrome(service=service)
        driver.get("http://127.0.0.1:5000/")

        driver.implicitly_wait(10)
        input_elem = driver.find_element(By.ID, 'email_input')

        input_elem.clear()

        input_elem.send_keys("test@test.co")

        input_elem.submit()

        driver.implicitly_wait(10)
        logout = driver.find_element(By.ID, "logout")
        logout.click()
        assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source

        driver.close()
    else:
        print('NOT IN TESTING MODE')
