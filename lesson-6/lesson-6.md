# Урок 6. Scrapy. Парсинг фото и файлов

важное

Платформа для сбора информации с дополнительными инструментами:
* асинхронность
* готовые шаблоны
* многопоточность

Под урок создаем отдельный проект с `new environment using` - не зависящее от глобального окружения.
`pip install scrapy`

* Создается проект из консоли: `scrapy startproject jobparser .`
* создадим паука - приложение которое занимается парсингом. `scrapy genspider hhru hh.ru` название по домену (gb.ru)

Прелесть фреймворков в том что уже заточен под сборку с шаблонами, он ООП, большая часть работы сделана за нас.


settings.py
```python
user_agent = `chrome:version`
robotstxt_obey = False
cookies_enabled = True
LOG_LEVEL = 'DEBUG'
```
время ответа от сервера 400 мс, поэтому все запросы в секунду он не выполнит. поэтому праметр concurent_request следует начинать с 8
LOG_LEVEL - внутренняя система логирования дает большую информацию чем pycharm.

hhru.py
скрапи не пускает своих пауков на сторонние домены.

чтобы запустить проект `scrapy crawl hhru`

## Запуск приложения в режиме отладки

runner.py:
```python
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider

if __name__ == '__main__':
    crawler_settins = Settings()
    crawler_settins.setmodule(settings)
    
    process = CrawlerProcess(settings=crawler_settins)
    process.crawl(HhruSpider)
```

Теперь после запуска `runner.py` в режиме отладки можно установить точку останова и в консоли будем видеть внутреннее состояние любого объекта.

точка входа - на примере hh.ru, если мы будем собирать все, то сайт вернет всего 800 вакансий, а всего вакансий 15000.
Получается потери оргомные, однако, если мы опросим отдельно москву, отдельно питер, то потери резко сократятся.
Реально покрыть все вакансии, вот этими стартовыми ссылками.

1:12 - конец перерыва.