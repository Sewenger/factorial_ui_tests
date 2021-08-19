import logging
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Final, Optional, Tuple, TypeVar, Union

from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import By, WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

PAGE = TypeVar('PAGE')
VAR = Optional[Dict[str, Any]]
STR = Union[str, int, float]
logger = logging.getLogger(__package__)


class UserBy(dict):

    def __missing__(self, key):
        return 'xpath'


BY: Final = UserBy({
    'id': By.ID,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'name': By.NAME,
    'tag': By.TAG_NAME,
    'class': By.CLASS_NAME,
    'css': By.CSS_SELECTOR
})
NUMBER = Union[int, float]


class MetaPage(metaclass=ABCMeta):
    timeout = 30

    @property
    @abstractmethod
    def page_key(self) -> str:
        ...

    @property
    @abstractmethod
    def locators(self) -> Dict[str, str]:
        ...

    def __init__(self, host: str, driver: Remote):
        self.host = host.rstrip('/')
        self.driver = driver

    def _get_locator(self, key: str) -> Tuple[str, str]:
        locator_type, locator = self.locators[key]
        return BY[locator_type], locator

    @property
    def url(self) -> str:
        return f'{self.host}{self.page_key}'

    def get(self):
        self.driver.get(self.url)

    def check_url(self, timeout: Optional[NUMBER] = None):
        WebDriverWait(self.driver, timeout or self.timeout).until(ec.url_contains(self.url))

    def wait_element(self, key: str, conditions: type, *, timeout: Optional[NUMBER] = None) -> WebElement:
        return WebDriverWait(
            self.driver, timeout or self.timeout
        ).until(
            conditions(self._get_locator(key)),
            message=f'Not Found Locator {key}'
        )

    def find_element(self, key: str, *, timeout: Optional[NUMBER] = None):
        return self.wait_element(key, ec.presence_of_element_located, timeout=timeout)

    def clear_text(self, element: Optional[WebElement] = None, key: Optional[str] = None) -> WebElement:
        if not element and key:
            element = self.find_element(key)
        element.clear()
        return element

    def enter_text(self, text: STR, element: Optional[WebElement] = None, key: Optional[str] = None, *,
                   insert: bool = True, clear: bool = False) -> WebElement:
        if not element and key:
            element = self.find_element(key)
        if clear:
            self.clear_text(element=element)
        text = str(text)
        element.send_keys(text) if insert else [element.send_keys(char) for char in text]
        return element

    def get_text(self, key: str) -> str:
        element = self.find_element(key=key)
        return element.text.strip()

    def wait_text(self, key: str, text: str, *, timeout: Optional[NUMBER] = None, msg: Optional[str] = None) -> None:
        WebDriverWait(
            self.driver, timeout or self.timeout
        ).until(
            ec.text_to_be_present_in_element(self._get_locator(key), text), message=msg
        )

    def click(self, key: str, *, timeout: Optional[NUMBER] = None) -> WebElement:
        element = self.wait_element(key, ec.element_to_be_clickable, timeout=timeout)
        element.click()
        return element
