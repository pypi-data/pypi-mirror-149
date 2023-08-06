import redis
import pickle


class ParamServer:
    def __init__(self, name, devices, args_from_dev, ip="localhost", port=6379):
        '''Parameters Server aggregating weight/gradient

        :param name: Name of this device treated as symbol of this device (must be unique)
        :type name: str

        :param devices: device participate in federated training
        :type devices: list

        :param args_from_dev: args to be received from devices
        :type args_from_dev: list

        :param ip: ip of redis server
        :type ip:str

        :param port: port redis server
        :type port:int

        :return Instance of device
        '''
        self.__conn = redis.Redis(host=ip, port=port, db=0)
        self.__channel = self.__set_channel(devices, args_from_dev)
        self.__ps = self.__conn.pubsub()
        self.__ps.subscribe(self.__channel)

        self.name = name
        self.devs = devices

    def __set_channel(self, devices, args):
        channel = tuple()
        for device in devices:
            channel += (f"grad_from_dev:{device}", f"weight_from_dev:{device}")
        if args is None:
            return channel
        for device in devices:
            for arg in args:
                channel += (f"{arg}_from_dev:{device}",)
        return channel

    def set_from_arg(self, arg, device):
        self.__ps.subscribe(f"{arg}_from_dev:{device}")

    def get_channel(self):
        return self.__ps.channels

    def send_grad(self, grad):
        grad = pickle.dumps(grad)
        return self.__conn.publish(f"grad_from_ps:{self.name}", grad)
        # return self.__conn.set("grad", grad)

    def send_weight(self, w):
        w = pickle.dumps(w)
        return self.__conn.publish(f"weight_from_ps:{self.name}", w)
        # return self.__conn.set("weight", w)

    def send(self, arg, value):
        value = pickle.dumps(value)
        return self.__conn.publish(f"{arg}_from_ps:{self.name}", value)

    def read(self, dev, arg):
        for item in self.__ps.listen():
            if item["channel"].decode() == f"{arg}_from_dev:{dev}" and item["type"] == "message":
                return pickle.loads(item["data"])

    def set(self, arg, value):
        self.__conn.set(arg, value)

    def get(self, arg):
        self.__conn.get(arg)
