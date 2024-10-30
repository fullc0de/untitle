import socketio

# Socket.IO 클라이언트 인스턴스 생성
sio = socketio.Client()

# 연결 이벤트 핸들러
@sio.event
def connect():
    print("Socket.IO 서버에 연결되었습니다!")

# 연결 끊김 이벤트 핸들러
@sio.event
def disconnect():
    print("서버와의 연결이 끊어졌습니다.")

# 메시지 수신 이벤트 핸들러
@sio.on('message')
def on_message(data):
    print("메시지를 수신했습니다:", data)

# 특정 이벤트 이름을 사용하는 이벤트 핸들러
@sio.on('custom_event')
def on_custom_event(data):
    print("custom_event 수신:", data)

# Socket.IO 서버에 연결
sio.connect('http://localhost:8000')  # 여기에 서버 URL을 입력하세요.

# 메시지 전송 예제
sio.emit('message', 'Hello, Socket.IO Server!')

# 이벤트 전송 예제
sio.emit('custom_event', {'key': 'value'})

# 연결을 유지하기 위해 대기
sio.wait()

