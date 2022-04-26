# BusPay2000
## Инструкция

Используемые фреймворки:
-  Bootstrap - для фронтенда
-  Flask - для бекенда

Используемый язык программирования:
-  Python 3.10.4

Необходимые библиотеки находятся в requriments.txt

Запуск:
1. Склонировать репозиторий себе
2. Создать виртуальное окружение (для windows)
2. python -m pip install virtualenv
3. python -m veirtalenv venv
4. venv\scripts\activate
5. cd .\BusPay2000
6. Установить зависимости "python -m pip install -r .\requriments.txt"
7. Запуск "python run.py"

Сброс БД:
1. Python bd.py (Удаление существующей бд и создание новой)
2. Или при запущенном приложении в браузере пройти по адресу /flush


BusPay2000 - пакет со всеми модулями.
run.py - исполняемый файл
В пакете BusPay2000 находятся:
- routes.py
  Отвечает за обработку всех ссылок .
- models.py
  Отвечает за репрезентацию сущностей базы данных в коде питона
- forms.py
  Отвечает за обработку форм, на основе которых генерируется html-формы для пользователей
- \__init__.py
  Отвечает за настройку фреймворка

https://buspay2000.herokuapp.com/ 