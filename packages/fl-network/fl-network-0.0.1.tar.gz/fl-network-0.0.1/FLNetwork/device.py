import redis
import pickle


class Device:
    def __init__(self, name, server, peers, args_from_ser, args_from_peer, ip="localhost", port=6379):
        '''Local Device training sub-model

        :param name: name of this device treated as symbol of this device (must be unique)
        :type name: str

        :param server: name of target parameters server
        :type server: str

        :param peers: device peers participate in federated training
        :type peers: list

        :param args_from_ser: args to be received from parameters server
        :type args_from_ser: list

        :param args_from_peer: args to be received from peer
        :type args_from_peer: list

        :param ip: ip of redis server
        :type ip:str

        :param port: port redis server
        :type port:int

        :return Instance of device
        '''
        self.__conn = redis.Redis(host=ip, port=port, db=0)
        self.__peers_channel = self.__set_dev_channel(peers, args_from_peer)
        self.__ser_channel = self.__set_ser_channel(server, args_from_ser)
        if self.__peers_channel is None:
            self.__channel = self.__ser_channel
        else:
            self.__channel = self.__ser_channel + self.__peers_channel
        self.__ps = self.__conn.pubsub()
        self.__ps.subscribe(self.__channel)

        self.name = name
        self.server = server
        self.peers =peers

    def __set_ser_channel(self, server, args):
        channel = tuple()
        for arg in args:
            channel += (f"{arg}_from_ps:{server}",)
        return channel

    def __set_dev_channel(self, peers, args=None):
        channel = tuple()
        if args is None:
            return None
        for peer in peers:
            for arg in args:
                channel += (f"{arg}_from_dev:{peer}",)
        return channel

    def set_from_arg(self, arg, dev_ser, is_server=False):
        if not is_server:
            self.__ps.subscribe(f"{arg}_from_dev:{dev_ser}")
        else:
            self.__ps.subscribe(f"{arg}_from_ps:{dev_ser}")

    def get_channel(self):
        return self.__ps.channels

    def send_grad(self, grad):
        grad = pickle.dumps(grad)
        return self.__conn.publish(f"grad_from_dev:{self.name}", grad)
        # return self.__conn.set("grad", grad)

    def send_weight(self, w):
        w = pickle.dumps(w)
        return self.__conn.publish(f"weight_from_dev:{self.name}", w)
        # return self.__conn.set("weight", w)

    def send(self, arg, value):
        value = pickle.dumps(value)
        return self.__conn.publish(f"{arg}_from_dev:{self.name}", value)

    def read_dev(self, dev, arg):
        for item in self.__ps.listen():
            if item["channel"].decode() == f"{arg}_from_dev:{dev}" and item["type"] == "message":
                return pickle.loads(item["data"])

    def read_ser(self, ser, arg):
        for item in self.__ps.listen():
            if item["channel"].decode() == f"{arg}_from_ps:{ser}" and item["type"] == "message":
                return pickle.loads(item["data"])

    def set(self, arg, value):
        self.__conn.set(arg, value)

    def get(self, arg):
        self.__conn.get(arg)
