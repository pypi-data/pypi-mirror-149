from .core import AbstractLayout
from ..widgets.html import Div


class DivLayout(AbstractLayout):
    def __init__(self, _app, template_name="main", **kwargs):
        super().__init__(
            _app, Div(trame_app=_app), template_name=template_name, **kwargs
        )
