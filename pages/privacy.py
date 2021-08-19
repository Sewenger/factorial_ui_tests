from pages._page import MetaPage


class Privacy(MetaPage):
    page_key = "/privacy"
    locators = {
        'text': ('xpath', '//body'),
    }

    def chek_elements(self):
        self.wait_text(key='text', text='This is the privacy document. We are not yet ready with it. Stay tuned!')
