import os
import ssl
import pika


class QueueNotFoundException(Exception):
    def __init__(self, name:str) -> None:
	    super(QueueNotFoundException, self).__init__(
            f'{name} queue not found in environment variables, please register'
        )

class BaseClientException(Exception):
    def __init__(self, var:str) -> None:
	    super(BaseClientException, self).__init__(
            f'The environment variable {var} is required for operation'
        )

class BaseClientParameter:
    ATTRIBUTES = [
        'AMQP_USER',
        'AMQP_PASSWORD',
        'AMQP_BROKER_ID',
        'AWS_REGION',
        'AMQP_HOST',
    ]

    def __init__(self) -> None:
        for attr in BaseClientParameter.ATTRIBUTES:
            setattr(self, attr.lower(), os.getenv(attr, None))
        self._check()

    def _check(self) -> None:
        if self.amqp_user is None:
            raise BaseClientException('AMQP_USER')

        if self.amqp_password is None:
            raise BaseClientException('AMQP_USER')

        if self.amqp_broker_id is None and self.amqp_host is None:
            raise BaseClientException('AMQP_BROKER_ID or AMQP_HOST')

        if self.amqp_broker_id is not None and self.aws_region is None:
            raise BaseClientException('AWS_REGION')

class BaseClient:
    def __init__(self) -> None:
        self.parameters = BaseClientParameter()

        if self.parameters.amqp_broker_id is None:
            self._create_connection_to_local_instance()
        else:
            self._create_connection_to_amazon_mq()

    def get_service_queue(self, service_name:str) -> str:
        queue = os.getenv(f'{service_name.upper()}_QUEUE', None)
        if queue is None:
            raise QueueNotFoundException(queue)
        return queue

    def _create_connection_to_local_instance(self, socket_timeout:int=5, heartbeat:bool=False) -> None:
        parameters = pika.URLParameters(
            'amqp://{AMQP_USER}:{AMQP_PASSWORD}@{AMQP_HOST}'.format(
                AMQP_USER=self.parameters.amqp_user,
                AMQP_PASSWORD=self.parameters.amqp_password,
                AMQP_HOST=self.parameters.amqp_host,
            )
        )
        parameters.socket_timeout = socket_timeout
        parameters.heartbeat = heartbeat

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def _create_connection_to_amazon_mq(self) -> None:
        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        parameters = pika.URLParameters(
            'amqps://{AMQP_USER}:{AMQP_PASSWORD}@{AMQP_BROKER_ID}.mq.{AWS_REGION}.amazonaws.com:5671'.format(
                AMQP_USER=self.parameters.amqp_user,
                AMQP_PASSWORD=self.parameters.amqp_password,
                AMQP_BROKER_ID=self.parameters.amqp_broker_id,
                AWS_REGION=self.parameters.aws_region,
            )
        )
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()