# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dialog(Component):
    """A Dialog component.
A modal dialog component with optional buttons. Can be set to be draggable.

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    The child elements showed in the dialog.

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- actions (list of strings; optional):
    A list of actions to be displayed as buttons in the lower right
    corner of the dialog.

- actions_called (number; optional):
    A counter for how often actions have been called so far.

- backdrop (boolean; optional):
    Set to False if you do not want to have a backdrop behind the
    dialog.

- draggable (boolean; optional):
    Set to True if the dialog shall be draggable.

- full_screen (boolean; optional):
    Set to True to show the dialog fullscreen.

- last_action_called (string; optional):
    The name of the action that was called last.

- max_width (a value equal to: "xs", "sm", "md", "lg", "xl"; optional):
    Width of the dialog. Can be one of 'xs' | 'sm' | 'md' | 'lg' |
    'xl'.

- open (boolean; optional):
    States if the dialog is open or not.

- title (string; required):
    The title of the dialog."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, open=Component.UNDEFINED, max_width=Component.UNDEFINED, full_screen=Component.UNDEFINED, draggable=Component.UNDEFINED, title=Component.REQUIRED, backdrop=Component.UNDEFINED, actions=Component.UNDEFINED, last_action_called=Component.UNDEFINED, actions_called=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'actions', 'actions_called', 'backdrop', 'draggable', 'full_screen', 'last_action_called', 'max_width', 'open', 'title']
        self._type = 'Dialog'
        self._namespace = 'webviz_core_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'actions', 'actions_called', 'backdrop', 'draggable', 'full_screen', 'last_action_called', 'max_width', 'open', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id', 'title']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dialog, self).__init__(children=children, **args)
