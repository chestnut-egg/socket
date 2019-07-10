import os

from flask import Flask, render_template
from flask_socketio import SocketIO,emit
from threading import Lock
import random
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

text = ''

def background_thread():
    global text
    tool_log = '/home/ppg/tmp/tool.log'
    f = open(tool_log)
    socketio.emit('server_response',
                  {'data': text}, namespace='/test_conn')


    while True:
        socketio.sleep(2)

        tool_log = '/home/ppg/tmp/tool.log'
        fp = open(tool_log,'r')
        text = fp.read()
        fp.close()
        socketio.emit('server_response',
                      {'data': text}, namespace='/test_conn')

if __name__ == '__main__':
    socketio.run(app, debug=True)
