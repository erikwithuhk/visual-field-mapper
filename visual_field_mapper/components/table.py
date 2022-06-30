from .base_component import BaseComponent
from .typography import Text


class Cell(BaseComponent):
    def __init__(self, content):
        self.content = content
        super().__init__()

    def render(self, debug: bool = False, *args, **kwargs):
        text = Text(f"{self.content}")
        return super().render([text], debug=debug, *args, **kwargs)


class Table(BaseComponent):
    def __init__(self, data, headers=None):
        self.data = data
        self.headers = headers
        super().__init__()

    def render(self, debug: bool = False, *args, **kwargs):
        cell = Cell("Test")
        return super().render([cell], debug=debug, *args, **kwargs)


TABLE_EXAMPLE = Table(
    [["IN", -14.29], ["IT", -11.43]], headers=["Sector", "Average TD"]
)
