import socketio
from .config import Config
from json import dumps, loads, JSONEncoder, JSONDecoder
# from kafka import KafkaConsumer, KafkaProducer
from .redis import redis_cache


# producer = KafkaProducer(bootstrap_servers='rc1a-dv477guks4sitb1e.mdb.yandexcloud.net:9092',
                        # value_serializer=lambda v: dumps(v).encode('utf-8'), 
                        # compression_type="lz4", 
                        # linger_ms=5)

# producer = KafkaProducer(
#     bootstrap_servers=['rc1a-dv477guks4sitb1e.mdb.yandexcloud.net:9092','rc1b-k2eb8k0sebln2jsp.mdb.yandexcloud.net:9092','rc1c-nctc8hqesvbarhad.mdb.yandexcloud.net:9092'],
#     security_protocol="SASL_PLAINTEXT",
#     sasl_mechanism="SCRAM-SHA-512",
#     sasl_plain_password="P8xq1Dai9euKQCSX",
#     sasl_plain_username="kafka-user",
#       value_serializer=lambda v: dumps(v).encode('utf-8'), 
        # compression_type="lz4", 
        # linger_ms=5)

mgr = socketio.AsyncRedisManager(Config.REDIS_URL)
sio = socketio.AsyncServer(async_mode='asgi', client_manager=mgr, cors_allowed_origins=[])    
socket_app = socketio.ASGIApp(sio)

background_task_started = False

async def background_task():     
        while True:
                await sio.sleep(10)
                await sio.emit('signal',  {'status': 'ok'})

@sio.on("connect")
async def test_connect(sid, environ):
        global background_task_started
        if not background_task_started:
                sio.start_background_task(background_task)
                background_task_started = True
        await sio.emit('message', sid, room=sid)

@sio.on("packet")
async def packet(sid, data):
        print(data)
        await sio.emit("message", data)

@sio.on("/users")
async def image(sid, data):
        frame = data["image"]
        print(frame)
        user_id = data["user_id"]
        # (warnings, frame) = await producer.send("process_gpu", {"frame": frame, "user_id": user_id})
        await sio.emit("message", "Processed")

@sio.on("disconnect")
async def test_disconnect(sid):
        print ("Client Disconnected")
