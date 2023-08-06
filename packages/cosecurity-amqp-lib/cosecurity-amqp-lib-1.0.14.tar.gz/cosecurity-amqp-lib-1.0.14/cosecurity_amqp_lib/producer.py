import json
import numpy as np

from json import JSONEncoder
from typing import Any, Dict, Tuple
from cosecurity_amqp_lib.logger import logger
from cosecurity_amqp_lib.client import BaseClient


class ProducerEncoder(JSONEncoder):
    def default(self, obj:Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class ProducerChannel(BaseClient):
    def __init__(self, destination_service_name:str) -> None:
        super().__init__()
        self.destination_queue = self.get_service_queue(destination_service_name)

    def __enter__(self) -> Tuple[Any, str]:
        return self.channel, self.destination_queue

    def __exit__(self, type:Any, value:Any, traceback:Any) -> None:
        self.channel.close()
        self.connection.close()

class Producer:
    def send_message(self, destination:str, primitive:str, content:Dict[str, Any]) -> None:
        with ProducerChannel(destination) as (channel, destination_queue):
            channel.basic_publish(
                exchange='', 
                routing_key=destination_queue, 
                body=json.dumps(
                    obj={ 
                        'primitive': primitive, 
                        'content': content 
                    }, 
                    cls=ProducerEncoder
                )
            )
        
        logger.info(f'Sent to {destination}')
