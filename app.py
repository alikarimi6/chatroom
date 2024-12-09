from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<room>')
def chat(room):
    return render_template('chat.html', room=room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} وارد اتاق شد.", to=room)

@socketio.on('message')
def on_message(data):
    room = data['room']
    send(data['msg'], to=room)

@socketio.on('file')
def on_file(data):
    room = data['room']
    filename = data['filename']
    file_data = data['file']
    emit('file', {'filename': filename, 'file': file_data}, to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
