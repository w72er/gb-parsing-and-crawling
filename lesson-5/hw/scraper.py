# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver: webdriver.Chrome):
    driver.get('https://mail.ru/')
    element = driver.find_element(By.CSS_SELECTOR, 'input[name=login]')
    element.send_keys('study.ai_172')
    element = driver.find_element(By.CSS_SELECTOR, 'button.button')
    element.click()
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=password]'))
    )
    element.send_keys('NextPassword172#')
    element = driver.find_element(By.CSS_SELECTOR, 'button.second-button')
    element.click()


def get_next_element(href):
    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.llc'))
    )
    i = 0
    for element in elements:
        i_href = element.get_attribute('href')
        if i_href == href:
            return elements[i + 1] if i < len(elements) - 1 else None
            # return elements[i + 1]
        i += 1


def parse_emails(driver: webdriver.Chrome):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.llc'))
    )
    i = 0
    while element:
        href = element.get_attribute('href')
        # element.click()
        # email = get_email(driver)
        # print(f'{email["date"]}: {email["subject"]}')
        # driver.back()
        print(f'i: {i}')
        i += 1

        webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        element = get_next_element(href)


def get_email(driver: webdriver.Chrome):
    # от кого, дата отправки, тема письма, текст письма полный
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.letter-contact'))
    )
    contact = element.text
    element = driver.find_element(By.CSS_SELECTOR, '.letter__date')
    date = element.text
    element = driver.find_element(By.CSS_SELECTOR, '.thread__subject')
    subject = element.text
    element = driver.find_element(By.CSS_SELECTOR, '.letter__body')
    body = element.text
    return {
        'contact': contact,
        'date': date,
        'subject': subject,
        'body': body
    }


def get_all_email_links(driver: webdriver.Chrome):
    links = set()
    last_href = None
    while True:
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.llc'))
        )

        for element in elements:
            links.add(element.get_attribute('href'))

        href = elements[-1].get_attribute('href')
        if last_href == href:
            print('DONE')
            break
        else:
            last_href = href

        actions = ActionChains(driver)
        actions.move_to_element(elements[-1])
        actions.perform()

    return links


if __name__ == '__main__':
    # https://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome('./chromedriver.exe')
    login(driver)
    links = get_all_email_links(driver)
    links = list(links)
    print(f'len: {len(links)}')
    for link in links[:4]:
        driver.get(link)
        email = get_email(driver)
        pprint(email)
    driver.quit()

