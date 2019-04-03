#!/usr/bin/env python

import app
from waitress import serve
serve(app.app, host='0.0.0.0', port=5000)
