# %%
from bs4 import BeautifulSoup

# %%
from selene.core.config import *
from selene.core.element import Element


# %%
class ElementSoup(Element):
    def __init__(self, element, logger=None):
        Element.__init__(self, element, logger)
        self.attrs = element.attrs
        self.text = element.get_text()

    @classmethod
    def from_selene(cls, element_selene, logger=None):
        html = element_selene.element.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "lxml")
        return cls(element=soup.body, logger=logger)

    def find(self, *args, **kwargs):
        self.log(f'find: {"; ".join([str(arg) for arg in [*args]])}')
        el = self.element.find(*args, **kwargs)
        if el is None:
            return ElementSoupBlank()
        if not el.has_attr("href"):
            el.attrs["href"] = None
        return ElementSoup(el, self.logger)

    def find_all(self, *args, **kwargs):
        self.log(f'find_all: {"; ".join([str(arg) for arg in [*args]])}')
        els = []
        for el in self.element.find_all(*args, **kwargs):
            if not el.has_attr("href"):
                el.attrs["href"] = None
            els.append(ElementSoup(el, self.logger))
        return els

    def get_text(self):
        return self.text

    def has_attr(self, *args, **kwargs):
        return self.element.has_attr(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.element.get(*args, **kwargs)


# %%
class ElementSoupBlank(ElementSoup):
    def __init__(self):
        self.element = None
        self.attrs = {"href": None, "id": None, "aria-label": None}
        self.find = lambda *x: ElementSoupBlank()
        self.find_all = lambda *x: []
        self.text = None
        self.has_attr = lambda *x: False
        self.get = lambda *x: None
        self.get_text: lambda: None
