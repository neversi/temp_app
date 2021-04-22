import socketio

sio = socketio.Client()
sio.connect(
    "http://95.179.246.114:7500/ws", socketio_path="/ws/socket.io"
)


@sio.on("message")
def new_packet(packet):
    print("\nMessage: ", packet)


def call_back(data):
    print("\ncall-back", data)


while True:
    sio.sleep(5)
    msg = input("Message: ")
    sio.emit(
        "packet",
        msg
    )