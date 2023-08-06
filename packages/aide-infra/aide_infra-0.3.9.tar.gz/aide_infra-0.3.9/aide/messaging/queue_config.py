class RabbitClientConfiguration:
    def __init__(self,
                 username,
                 password,
                 host,
                 port,
                 exchange,
                 routing_key,
                 queue,
                 error_queue_name,
                 delay_queue="",
                 requeue_message_max_tries=3,
                 requeue_message_delay=120000,
                 prefetch_count=0,
                 retry_limit=5,
                 retry_wait=30):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.exchange = exchange
        self.routing_key = routing_key
        self.prefetch_count = prefetch_count
        self.connection_retry_limit = retry_limit
        self.connection_retry_wait = retry_wait
        self.queue = queue
        self.delay_queue = delay_queue
        self.requeue_message_max_tries = requeue_message_max_tries
        self.requeue_message_delay = requeue_message_delay
        self.error_queue_name = error_queue_name
