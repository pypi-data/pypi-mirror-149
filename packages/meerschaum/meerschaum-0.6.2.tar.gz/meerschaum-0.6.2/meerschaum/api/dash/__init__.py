#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Build the Dash app to be hooked into FastAPI.
"""

from __future__ import annotations
import uuid
from meerschaum.utils.typing import List, Optional
from meerschaum.config.static import _static_config
from meerschaum.api import (
    app as fastapi_app,
    debug,
    _get_pipes,
    get_pipe as get_api_pipe,
    pipes as api_pipes,
    get_api_connector,
    endpoints,
)
from meerschaum.utils.packages import attempt_import, import_dcc, import_html
from meerschaum.connectors.parse import parse_instance_keys
flask_compress = attempt_import('flask_compress', lazy=False)
import pkg_resources
from collections import namedtuple
_pkg_resources_get_distribution = pkg_resources.get_distribution
_Dist = namedtuple('_Dist', ['version'])
def _get_distribution(dist):
    """Hack for flask-compress.
    """
    if dist == 'flask-compress':
        return _Dist(flask_compress.__version__)
    return _pkg_resources_get_distribution(dist)
pkg_resources.get_distribution = _get_distribution
dash = attempt_import('dash', lazy=False)
import warnings
### Suppress the depreciation warnings from importing enrich.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    enrich = attempt_import('dash_extensions.enrich', lazy=False)
html, dcc = import_html(), import_dcc()
from meerschaum.api.dash.components import location

active_sessions = {}
running_jobs = {}
running_monitors = {}
stopped_jobs = {}
stopped_monitors = {}

stylesheets = [
    '/static/css/bootstrap.min.css',
    '/static/css/dbc_dark.css',
    '/static/css/dash.css',
    #  '/static/js/node_modules/xterm/css/xterm.css',
]
scripts = ['/static/js/node_modules/xterm/lib/xterm.js']
dash_app = enrich.DashProxy(
    __name__,
    title = 'Meerschaum Web',
    requests_pathname_prefix = endpoints['dash'] + '/',
    external_stylesheets = stylesheets,
    #  external_scripts = scripts,
    update_title = None,
    #  prevent_initial_callbacks = True,
    suppress_callback_exceptions = True,
    transforms = [
        enrich.TriggerTransform(),
        enrich.MultiplexerTransform(),
        enrich.ServersideOutputTransform(),
        #  enrich.NoOutputTransform(),
    ],
)

dash_app.layout = html.Div([
    location,
    dcc.Store(id='session-store', storage_type='session', data={}),
    html.Div([], id='page-layout-div')
])

import meerschaum.api.dash.pages as pages
import meerschaum.api.dash.callbacks as callbacks

fastapi_middleware_wsgi = attempt_import('fastapi.middleware.wsgi')
fastapi_app.mount(endpoints['dash'], fastapi_middleware_wsgi.WSGIMiddleware(dash_app.server))
