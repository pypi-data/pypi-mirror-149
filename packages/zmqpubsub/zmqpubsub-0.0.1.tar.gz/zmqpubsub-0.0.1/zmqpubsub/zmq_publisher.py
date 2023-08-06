import zmq


class Publisher:

    def __init__(self, ip, port):
        self.publisher_zmq = ZMQPublisher(ip, port)
        self.start()

    def start(self):
        self.publisher_zmq.start()


class ZMQPublisher:

    def __init__(self, ip, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.bind = 'tcp://' + ip + ':' + port

    def start(self):
        self.socket.bind(self.bind)

    def publish(self, topic: str, payload):
        self.socket.send_string(f"{topic}:{payload}")
