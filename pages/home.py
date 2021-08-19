from pages._page import MetaPage
from pages.privacy import Privacy
from pages.qxf2 import Qxf2
from pages.terms import Terms
from utils.func import factorial, wait_for


class Home(MetaPage):
    page_key = '/'
    locators = {
        'input': ('id', 'number'),
        'submit': ('id', 'getFactorial'),
        'privacy_link': ('xpath', '//p[contains(@class, "wor_copyright")][1]/a[@href="/privacy"]'),
        'terms_link': ('xpath', '//p[contains(@class, "wor_copyright")][1]/a[@href="/terms"]'),
        'qxf2_link': ('xpath', '//p[contains(@class, "wor_copyright")][2]/a[contains(@href, "https://www.qxf2.com/")]'),
        'result': ('id', 'resultDiv'),
        'title': ('tag', 'h1')
    }

    def _new_page(self, key: str, page):
        self.click(key=key)
        page = page(self.host, self.driver)
        page.check_url()
        return page

    def go_to_terms(self):
        return self._new_page(key='terms_link', page=Terms)

    def go_to_privacy(self):
        return self._new_page(key='privacy_link', page=Privacy)

    def go_to_qxf2(self):
        return self._new_page(key='qxf2_link', page=Qxf2)

    def go_to(self, page_key: str):
        if method := getattr(self, f'go_to_{page_key}', None):
            return method()
        raise ValueError(f'not found {page_key=}')

    def chek_elements(self):
        self.wait_text(key='title', text='The greatest factorial calculator!')
        for key in ('input', 'submit', 'privacy_link', 'terms_link', 'qxf2_link'):
            self.find_element(key=key)

        wait_for(lambda: not self.get_text(key='result'))

    def check_factorial(self, x: str):
        self.enter_text(x, key='input', clear=True)
        self.click(key='submit')
        text = wait_for(lambda: self.get_text('result'))
        _, result = text.split(':')
        assert float(result) == factorial(int(x))

    def check_negative_data(self, value, text):
        self.enter_text(value, key='input', clear=True)
        self.click(key='submit')
        self.wait_text(key='result', text=text, timeout=5, msg=f'Wait {text=}')
