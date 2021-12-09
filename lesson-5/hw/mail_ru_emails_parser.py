from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MailRuEmailsParser:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        # https://chromedriver.chromium.org/downloads
        self.driver = webdriver.Chrome('./chromedriver.exe')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def login(self):
        self.driver.get('https://mail.ru/')
        element = self.driver.find_element(By.CSS_SELECTOR, 'input[name=login]')
        element.send_keys('study.ai_172')
        element = self.driver.find_element(By.CSS_SELECTOR, 'button.button')
        element.click()
        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=password]'))
        )
        element.send_keys('NextPassword172#')
        element = self.driver.find_element(By.CSS_SELECTOR, 'button.second-button')
        element.click()

    def get_all_email_links(self):
        links = set()
        last_href = None
        while True:
            elements = WebDriverWait(self.driver, 20).until(
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

            actions = ActionChains(self.driver)
            actions.move_to_element(elements[-1])
            actions.perform()

        return list(links)

    @staticmethod
    def get_email_id_from_email_url(url: str) -> str:
        return url.split('/')[4]

    def get_email(self, link: str):
        self.driver.get(link)
        email_id = self.get_email_id_from_email_url(link)
        # от кого, дата отправки, тема письма, текст письма полный
        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.letter-contact'))
        )
        contact = element.text
        element = self.driver.find_element(By.CSS_SELECTOR, '.letter__date')
        date = element.text
        element = self.driver.find_element(By.CSS_SELECTOR, '.thread__subject')
        subject = element.text
        element = self.driver.find_element(By.CSS_SELECTOR, '.letter__body')
        body = element.text
        return {
            'id': email_id,
            'contact': contact,
            'date': date,
            'subject': subject,
            'body': body
        }


if __name__ == '__main__':
    with MailRuEmailsParser() as parser:
        parser.login()
        links = parser.get_all_email_links()
        print(f'len: {len(links)}')
        for link in links[:4]:
            email_id = parser.get_email_id_from_email_url(link)
            email = parser.get_email(link)
            print(f'{email["id"]} {email["date"]} {email["contact"]} {email["subject"][:30]}')
    print('with done')
