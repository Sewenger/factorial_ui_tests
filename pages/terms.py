import math
from typing import Dict

from pages._page import MetaPage
from utils.func import factorial, wait_for


class Terms(MetaPage):
    page_key = "/terms"
    locators = {
        'text': ('xpath', '//body'),
    }

    def chek_elements(self):
        self.wait_text(
            key='text',
            text='This is the terms and conditions document. We are not yet ready with it. Stay tuned!'
        )
