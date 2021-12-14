```python
import requests

url = ''
response = requests.get(url)
with open('file.jpg', 'wb') as f:
    f.write(response.content)
```

```python
import wget

wget.download('url')
```

## scrapy

Определимся с точкой входа.

В `runner.py` `process.crawl(AwitoSpidder, search='клюшка')` и в конструктор паука передастся параметр `search`.
Поскольку конструктор наследуется из базового класса, то мы его создадим заново.
```python
def __init__(self, search, kwargs):
    super().__init(**kwargs)
    self.start_urls = [f'https://avito.ru?search={search}']
```

```python
# у ссылки не надо получать href, чтобы перейти по ней
yield response.follow(link, callback=self.parse_page)
```

Задача паука спарсить данные, а обработать в другом месте.
Ищи закономерности в маленьких картинках и больших.

## скачивание по ссылкам

в scrapy есть уже пайплайны для скачивания.
```python
from scrapy.pipelines.images import  ImagesPipeline

class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_request(self):

```

```python
ITEM_PIPELINES = {
    'first': priority,
    'second': priority -100
}

IMAGES_STORE = 'photos'
```

```shell
pip install pillow
```

```python
if item['photos']:
    for photo in item['photos']:
        try:
            yield scrapy.Request(photo)
        except Exception as e:
            print(e)
```

Но как не потерять связь между фото и объявлением
Мы не знаем будет ли наш pipeline опследним, поэтому всегда возвращаем  `return`

## увеличиваем от 15-30%

```python
loader = ItemLoader()
```

Маленькая обработка (замена символов) в пред обработке или пост. А сложная логика в пайплайнах.

Сохранение в базу в отдельном пайплайне.

Авито блокирует на час.


## ДЗ

в разные папки

внутри file_path() что внутри AvitoPhotosPipeline(ImagesPipeline)