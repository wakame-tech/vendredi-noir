#!/usr/bin/env python

"""
@author: wakame-tech
"""

import os
from events import app, socketio

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, debug=True, host='0.0.0.0', port=port, threaded=True)
