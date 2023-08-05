# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashFlow(Component):
    """A DashFlow component.


Keyword arguments:

- edgeLists (list; optional)

- nodeLists (list; optional)"""
    @_explicitize_args
    def __init__(self, nodeLists=Component.UNDEFINED, edgeLists=Component.UNDEFINED, **kwargs):
        self._prop_names = ['edgeLists', 'nodeLists']
        self._type = 'DashFlow'
        self._namespace = 'dash_flow'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['edgeLists', 'nodeLists']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashFlow, self).__init__(**args)
