Урок 8. Работа с данными

рассмотрим низкоуровневое взаимодействие

сможем ли мы повторить авторизацию.
fetch/xhr + сохранять журнал
Хакинг какой-то: проверить, а получится ли их передать и авторизоваться.

csrf-защита берется из самой первой страницы.

req.follow - чтобы в рамках сессии, а не scrap.req...

На разных ступенях собираем данные, и чтобы их не потерять, их можно внутри каждого yield их передавать с помощью параметра cb_kwargs={'uname': ''}, и затем используем параметр с тем же именем 'uname'
Используя подход с передачей данных, мы понимаем какого пользователя мы парсим.

graphql
используется для получения публикаций, graphql много где распространен.
id - user
first - кол=во страниц
after - query.

1:16 https://gb.ru/lessons/184655

## Как определить параметр after?

after = end_cursor.

`id` - лучше брать из структур, где есть поля что показывают, что этот `id` пользователя.

`deepcopy` - поскольку параметры передаются по ссылке в функцию которые вызываются параллельно, и поскольку функции изменяют содержимое по ссылке, то они будут собирать неверную информацию.

## управляемые задерки

autothrottle_enabled = True

Если сервер дольше отвечает на запросы `scrapy` увеличивает задержку.

Автор описал параметры, обрисовал их влияние на процесс, а после показал по логам.

Если нет области применения знаний, то они у вас на долго не задержатся. Поэтому не тратьте на уроки много времени.

подписчики берите get-запросы
Ваши подписки - инкременты

Если сложите в базу данных все в одну кучу, тоесть не спроектируете базу, то запросы из последних задач, будут кривыми. Идея: зайди с последних пунктов.

Запросы к api инстаграма выполняются лишь с user-agent инстаграмм.

Автор: представляет как реализовать что просят в вопросе, и находит ответ на своих знаниях. о ста пауках на разных серверах.

## домашняя работа zip



