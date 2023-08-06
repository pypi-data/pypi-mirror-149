from .core import AbstractElement

# -----------------------------------------------------------------------------
# TrameApp
# -----------------------------------------------------------------------------
# SKIP: built-in client not to be use within a server template

# -----------------------------------------------------------------------------
# TrameClientStateChange
# -----------------------------------------------------------------------------
class ClientStateChange(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-client-state-change", children, **kwargs)
        self._attr_names += ["value"]
        self._event_names += ["change"]


# -----------------------------------------------------------------------------
# TrameClientTriggers
# -----------------------------------------------------------------------------
class ClientTriggers(AbstractElement):
    def __init__(self, ref="trame_triggers", children=None, **kwargs):
        self.__name = ref
        super().__init__("trame-client-triggers", children=None, ref=ref, **kwargs)
        self._attr_names += ["ref"]
        self._event_names += list(kwargs.keys())

    def call(self, method, *args):
        self._app.js_call(self.__name, "emit", method, *args)


# -----------------------------------------------------------------------------
# TrameConnect
# -----------------------------------------------------------------------------
class Connect(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-connect", children, **kwargs)
        self._attr_names += [
            "name",
            "config",
            ("use_url", "useUrl"),
        ]
        self._event_names += [
            ("trame_template_change", "trameTemplateChange"),
            ("state_change", "stateChange"),
        ]


# -----------------------------------------------------------------------------
# TrameLifeCycleMonitor
# -----------------------------------------------------------------------------
class LifeCycleMonitor(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-life-cycle-monitor", children, **kwargs)
        self._attr_names += [
            "name",
            "type",
            "value",
            "events",
        ]


# -----------------------------------------------------------------------------
# TrameLoading
# -----------------------------------------------------------------------------
class Loading(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-loading", children, **kwargs)
        self._attr_names += [
            "message",
        ]


# -----------------------------------------------------------------------------
# TrameMouseTrap
# -----------------------------------------------------------------------------
class MouseTrap(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("trame-mouse-trap", **kwargs)
        self._attributes["_trame_mapping"] = ':mapping="trame__mousetrap"'
        self._event_names += [*kwargs.keys()]

    def bind(self, keys, event_name, stop_propagation=False, listen_to=None):
        self._event_names += [event_name]
        entry = {
            "keys": keys,
            "event": event_name,
        }
        if stop_propagation:
            entry["stop"] = 1

        if listen_to:
            entry["listen"] = listen_to
        self._app.state.trame__mousetrap.append(entry)

    def reset(self):
        self._app.state.trame__mousetrap = []


# -----------------------------------------------------------------------------
# TrameServerTemplate
# -----------------------------------------------------------------------------
class ServerTemplate(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-server-template", children, **kwargs)
        self._attr_names += [
            ("name", "templateName"),
            ("use_url", "useUrl"),
            ("url_key", "urlKey"),
        ]

# -----------------------------------------------------------------------------
# TrameSizeObserver
# -----------------------------------------------------------------------------
class StateResolver(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-size-observer", children, **kwargs)
        self._attr_names += [
            "name",
        ]
        self._event_names += [
            "change",
        ]


# -----------------------------------------------------------------------------
# TrameStateResolver
# -----------------------------------------------------------------------------
class StateResolver(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("trame-state-resolver", children, **kwargs)
        self._attr_names += [
            "names",
        ]