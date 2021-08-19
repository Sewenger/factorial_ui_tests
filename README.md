# factorial_ui_tests

## Установить pipenv

```bash
pip install -U pipenv
# для unix подобных систем как правило
pip3 install -U pipenv
```

## Создание окружения

```bash
# Перейти в корень проекта
cd {path to the project}/factorial_ui_tests

# Создать окружение
pipenv --python 3.9

# Установить зависимости
pipenv install
```

## Активация виртуального окружения

```bash
# Перейти в корень проекта
cd {path to the project}/factorial_ui_tests

# Активировать
pipenv shell

# Деактивировать
exit
```


## Использование selenoid

Зависимости для использования selenoid

* `docker`
* `docker-compose`
* Любой интерпретатор bash скриптов (Для windows подходит `git-bash`)

Развернуть контейнеры

```bash
bash selenoid.sh up
```

Свернуть контейнеры

```bash
bash selenoid.sh down
```

> Для использования selenoid при запуске тестов необходимо передать параметр `--driver=selenoid`
> или в файле `pytest.ini` указать `driver = selenoid`


## Использование chromedriver

Для использования chromedriver нужно бинарный файл положить в корень проекта

> В файле `pytest.ini` в поле `driver` нужно указать любое значение не равное `selenoid` ex: `driver = webdriver`

## Параметры запуска

```bash
--host HOST - Хост тестируемого ресурса без схемы

--login VALUE - login для доступа к хосту

--password VALUE - password для доступа к хосту

--driver VALUE - Тип драйвера (selenoid/webdriver)
```


## Запуск всех тестов

```bash
pytest --host=example.com --login=my_login --password=my_password --driver=selenoid
```