import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Departement(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            r'C:\Users\nath\PycharmProjects\Conduite-de-tests\StoreManager\test_selenium\chromedriver.exe')

    def test_modify_dep_name(self):
        '''
        Test to modify the first departement name of departement page to 'football de rue'
        '''

        self.connexion()  # connect as admin

        driver = self.driver
        driver.get("http://127.0.0.1:8000/StoreManager/departement")

        element = driver.find_element_by_css_selector(
            '#content > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > input[type=text]')  # find input text element

        old_text = element.get_attribute("value")  # get text value

        new_text = "football de rue"
        driver.execute_script("arguments[0].setAttribute('value', '" + new_text + "')", element)  # set new value

        driver.find_element_by_xpath(
            '//*[@id="content"]/div/table/tbody/tr[2]/td[1]/input').click()  # click on checkbox

        driver.find_element_by_xpath('//*[@id="button"]/input[2]').click()  # click on modify button

        element = driver.find_element_by_css_selector(
            '#content > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > input[type=text]')

        new_text = element.get_attribute("value")  # get new dep name modified

        self.assertNotEqual(old_text, new_text)  # we check if the departement name is correctly modify

    def connexion(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/StoreManager/departement")

        element = driver.find_element_by_xpath('//*[@id="id_username"]')
        element.send_keys('admin')

        element = driver.find_element_by_xpath('//*[@id="id_password"]')
        element.send_keys('password')

        element = driver.find_element_by_xpath('/html/body/form/input[2]').click()

    def tearDown(self):
        driver = self.driver

        element = driver.find_element_by_css_selector(
            '#content > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > input[type=text]')  # find input text element

        new_text = "football de rue"
        driver.execute_script("arguments[0].setAttribute('value', '" + new_text + "')", element)  # set new value

        driver.find_element_by_xpath(
            '//*[@id="content"]/div/table/tbody/tr[2]/td[1]/input').click()  # click on checkbox

        driver.find_element_by_xpath('//*[@id="button"]/input[2]').click()  # click on modify button

        self.driver.close()


if __name__ == "__main__":
    unittest.main()
