class AbstractLayout:
    def __init__(self, _app, _root_elem, template_name="main", **kwargs):
        self._app = _app
        self._current_root = _root_elem
        self._template_name = f"trame__template_{template_name}"
        self._app.state[self._template_name] = ""

    @property
    def root(self):
        """
        Top level Vue component. Useful for providing / injecting into children components. Setting makes old root child of new root.
        """
        return self._current_root

    @root.setter
    def root(self, new_root):
        if new_root and self._current_root != new_root:
            new_root.children += [self._current_root]
            self._current_root = new_root

    @property
    def html(self):
        """
        Compute corresponding layout String which represent the html part.
        """
        return self.root.html

    @property
    def app(self):
        return self._app

    @property
    def state(self):
        """
        Return App state as a dictionary or extend it when setting.
        This is a safe way to build the state incrementaly.
        >>> layout.state = { "a": 1, "b": 2 }
        >>> print(layout.state)
        ... {"a": 1, "b": 2}
        >>> layout.state = { "c": 3, "d": 4 }
        >>> print(layout.state)
        ... {"a": 1, "b": 2, "c": 3, "d": 4}
        """
        return self._app.state

    def flush_content(self):
        """Push new content to client"""
        self.app.state[self._template_name] = self.html

    # -------------------------------------------------------------------------
    # Resource manager
    # -------------------------------------------------------------------------

    def __enter__(self):
        self.root.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.root.__exit__(exc_type, exc_value, exc_traceback)
        self.flush_content()
