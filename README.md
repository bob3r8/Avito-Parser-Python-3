# Avito-Parser-Python-3
Программа для парсинга сайта avito.ru по поисковому запросу и городу
На данный момент доступна только версия без GUI.
Для работы программы необходимы следующие библиотетки:
```
Selenium
BeautifulSoup4
csv
```
Для парсинга по собственному запросу измените следующие переменные в parsing.py:
```
CITY = 'rossiya'    # Город
Q = 'razer'         # Запрос
```
И запустите программу:
##### Windows:
    python parsing.py
##### Linux:
    python3 parsing.py
Результат будет сохранен в файл названным так же, как и запрос и расширением .csv. Удобнее всего просматривать в MC Excel <br>
У данного приложения есть так же ветка с мультипотоковым парсингом, однако та версия не работает из-за капчи. Желающие могут дописать собственный обход капчи или воспользоваться сервисами по её решению. <br>
