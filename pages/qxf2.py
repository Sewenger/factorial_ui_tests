from pages._page import MetaPage


class Qxf2(MetaPage):
    page_key = "https://qxf2.com/"
    locators = {
        'head': ('xpath', '//a/h1'),
    }

    @property
    def url(self) -> str:
        return self.page_key

    def chek_elements(self):
        self.wait_text(key='head', text='QA for startups')
