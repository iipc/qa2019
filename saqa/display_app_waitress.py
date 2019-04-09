#!/usr/bin/env python

import display_app
from waitress import serve

serve(display_app.app, host='0.0.0.0', port=5000)
