from pathlib import Path
from typing import Union, Final

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from selenium import webdriver
from pages.home import Home

ROOT_PATH: Final[Path] = Path(__file__).parent.absolute()


def get_key(config: Config, key: str) -> str:
    return config.getoption(key) or config.getini(key)


def browser(config: Config) -> Union[webdriver.Remote, webdriver.Chrome]:
    value = get_key(config, 'driver')
    if value == 'selenoid':
        return webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities={
                'browserName': 'chrome',
                'browserVersion': 'latest',
                "selenoid:options": {
                    "screenResolution": '1920x1080x24',
                    "enableVNC": True,
                    "enableVideo": False,
                    "enableLog": False,
                    "sessionTimeout": "10m"
                }
            })
    path = ''
    if paths := list(ROOT_PATH.glob('chromedriver*')):
        path = str(paths[0])
    return webdriver.Chrome(executable_path=path)


def pytest_addoption(parser: Parser):
    group = parser.getgroup('Python selenium tests')
    _help = 'WebDriver setting webdriver/selenoid'
    group.addoption('--driver', metavar='VALUE', help=_help, default='', dest='driver')
    parser.addini('driver', help=_help, default='webdriver')

    _help = 'Testing host'
    group.addoption('--host', metavar='VALUE', help=_help, default='', dest='host')
    parser.addini('host', help=_help, default='')

    _help = 'host_login'
    group.addoption('--login', metavar='VALUE', help=_help, default='', dest='login')
    parser.addini('login', help=_help, default='')

    _help = 'host_password'
    group.addoption('--password', metavar='VALUE', help=_help, default='', dest='password')
    parser.addini('password', help=_help, default='')


@pytest.fixture(scope='module')
def driver_module(request) -> Union[webdriver.Remote, webdriver.Chrome]:
    """Возвращает драйвер 1 раз за модуль"""
    _driver = browser(request.config)
    yield _driver
    _driver.quit()


@pytest.fixture
def get_home_page(request, driver_module):
    login = get_key(request.config, 'login')
    password = get_key(request.config, 'password')
    host = get_key(request.config, 'host')
    url = f'https://{login}:{password}@{host}'
    home = Home(
        host=url,
        driver=driver_module
    )
    home.get()
    home.check_url()
    return home
