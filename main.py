from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Emit a message to the client on connect
    emit('server_response', {'data': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('client_event')
def handle_client_event(json):
    print('Received event: ' + str(json))
    emit('server_response', {'data': 'Message received'})


def background_task():
    while True:
        socketio.sleep(10)
        socketio.emit('server_response', {'data': 'Periodic message from server'})


if __name__ == '__main__':
    socketio.start_background_task(target=background_task)
    socketio.run(app, allow_unsafe_werkzeug=True, host='127.0.0.1', port=8080)
