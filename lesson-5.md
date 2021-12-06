# Selenium

Селениум ужен для:
* авторизация
* сбор данных после какиъ либо действий.

```shell
pip install selenium
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # все клавиши стандартной клавы
# webdriver - это каркас, теперь нужно конкретную реализацию скачать.
# кладем его в нашу директорию.
driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://gb.ru') # откроется окно
# смотрим на странице input с логином.
login = driver.find_element(By.ID, 'user_email')
login.send_keys('st@main.ru')

elem.send_keys(Keys.ENTER)

driver.find_element(By.CLASS_NAME, 'mn-dropdown-item__text')
# закрыть страницу
```

Не меняйте размер экрана никогда!
Ставим на отладку и затем 
На все элементы есть элементы управление более удобные чем клики.
```python
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.NAME, 'user[gender]'))
select.select_by_value("female")
gender = driver.find_element(By.NAME, 'user[gender]')
gender.submit()
driver.back()
driver.forward()
driver.refresh()
```

1&18

## Динамическая подгрузка.

Селениум нужен загрузить еще или далее

from selenium.webdriver.chrome.options import options

chrome_options = Options() - аргументы в документации
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome('.chromedriver', )
button.click()

Если вы будете кликать по ссылкам, то код может не дождаться загрузки элемента или страницы, поэтому надо вствить задержку.
* driver.implicitly_wait(10)
* неявное ожидание
  * EC.prisence_of_element_located
  * EC.prisence_of_element_to_be_clickable
* time.sleep(4)

from selenium.webdriver.support.ui import WebDriverWait
ExpectedConditions

wait = webDriverWait(driver, 10)
button = wait.until(EC.prisence_of_element_located)

articles = driver.fidn_elements(By.TAG_NAME, 'articles')

actions = ActionChains(driver)
actions.move_to_element(articles[-1])
actions.key_down(Keys.LEFT_CONTROL).key_down()
actions.perform()

нет событий когда мы узнаем когда подгрузится страница.

## Домашнее задание

Вариант 2 проще.
* пэйдж даун
* либо перекрутиться на пиксели

дождаться загрузки товаов
изучите как работает кнопка загрузки.

--
ссылки на письма.
Письма которые собираются исчезают, поэтому 
свойство текст читаем в единую строку.
сохранять можно в базу данных.

## домашняя работа

находите общее у сущностей, которые вы хотите парсить, возможно, у интересующего блока новостей будет красное время публикации. Обращайте внимание на стили, даты публикации.
//a[contains(@href, 'rubric=politics')]

Оси xpath используем когда нужно 
`ancestor::article`, когда разное количество узлов наверх.

популярность: бсуп -> xpath -> css-selectors.