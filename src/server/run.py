#!/usr/bin/env python

"""
@author: wakame-tech
"""

from events import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # socketio.run(app, host='0.0.0.0', port=8000, debug=True)
