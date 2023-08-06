
### Extensible network framework library for federated learning system

```python
from src.fedmlnetwork.device import Device
from src.fedmlnetwork.paramServer import ParamServer

if __name__ == '__main__':
    # setup()
    dev_01 = Device(name="dev_01",
                    server="param_sys", peers=["dev_02"],
                    args_from_ser=["weight", "grad"], args_from_peer=[])

    dev_02 = Device(name="dev_02",
                    server="param_sys", peers=["dev_01"],
                    args_from_ser=["weight", "grad"], args_from_peer=[])

    server = ParamServer(name="param_sys", devices=["dev_01", "dev_02"], args_from_dev=["weight", "grad"])


```

