import functools
import logging
import threading
import time
from typing import Callable

import pika
from pika.exchange_type import ExchangeType

from aide.messaging.exceptions import BaseDeterministicError, BaseEnvironmentalError, BaseUnknownError
from aide.messaging.queue_config import RabbitClientConfiguration

logger = logging.getLogger(__name__)


class Consumer(threading.Thread):
    def __init__(self, config: RabbitClientConfiguration):
        super().__init__(daemon=True)
        self.config = config
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        self._on_consumption_callback = None
        self._reconnect_counter = 0

    def set_callback(self, callback: Callable):
        """Set the callback for message consumption.
        Any consumed messages will trigger this callback from a dedicated worker thread."""
        self._on_consumption_callback = callback

    def _connect(self) -> pika.SelectConnection:
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.
        :rtype: pika.SelectConnection
        """
        credentials = pika.PlainCredentials(username=self.config.username,
                                            password=self.config.password)

        connection_params = pika.ConnectionParameters(
            host=self.config.host,
            port=self.config.port,
            credentials=credentials)

        return pika.SelectConnection(
            parameters=connection_params,
            on_open_callback=self._on_connection_open,
            on_open_error_callback=self._on_connection_open_error,
            on_close_callback=self._on_connection_closed)

    # Callbacks
    def _on_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.
        :param pika.SelectConnection _unused_connection: The connection
        """
        logger.info('Connection opened')
        self._open_channel()

    def _on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """

        logger.error('Connection open failed, reconnect in {} seconds. '
                     'Error: {}.'.format(self.config.connection_retry_wait, repr(err)))
        self._reconnect()

    def _on_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        :param pika.connection.Connection _unused_connection:
        The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.
        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            logger.warning('Connection closed, reopening in {} seconds. '
                           'Error: {}'.format(self.config.connection_retry_wait, repr(reason)))
            self._reconnect()

    def _on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.
        Since the channel is now open, we'll declare the exchange to use.
        :param pika.channel.Channel channel: The channel object
        """
        logger.info('Channel opened')
        self._reconnect_counter = 0
        self._channel = channel
        self._add_on_channel_close_callback()
        self._setup_exchange(self.config.exchange)

    def _on_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.
        :param channel: The closed channel
        :param Exception reason: why the channel was closed
        """
        logger.warning('Channel %i was closed: %s', channel, reason)
        self._close_connection()

    def _on_exchange_declareok(self, _unused_frame, userdata):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.
        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param str|unicode userdata: Extra user data (exchange name)
        """
        logger.info('Exchange declared: %s', userdata)
        self._setup_queue(self.config.queue)
        self._setup_delay_queue(self.config.delay_queue)
        self._setup_error_queue(self.config.error_queue_name)

    def _on_queue_declareok(self, _unused_frame, userdata):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.
        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        queue_name = userdata
        logger.info('Binding %s to %s with %s', self.config.exchange,
                    queue_name,
                    self.config.routing_key)
        cb = functools.partial(self._on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.config.exchange,
            routing_key=self.config.routing_key,
            callback=cb)

    def _on_bindok(self, _unused_frame, userdata):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will set the prefetch count for the channel.
        :param pika.frame.Method _unused_frame: The Queue.BindOk response frame
        :param str|unicode userdata: Extra user data (queue name)
        """
        logger.info('Queue bound: %s', userdata)
        self._set_qos()

    def _on_basic_qos_ok(self, _unused_frame):
        """Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.
        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame
        """
        logger.info('QOS set to: %d', self.config.prefetch_count)
        self._start_consuming()

    def _on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.
        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """
        logger.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def _on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        :param pika.channel.Channel _unused_channel: The channel object
        :param basic_deliver: basic_deliver method
        :param properties: properties
        :param bytes body: The message body
        """
        t = threading.Thread(target=self._run_message_callback,
                             args=(basic_deliver.delivery_tag, body, properties))
        t.start()

    def _on_cancelok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.
        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)
        """
        self._consuming = False
        logger.info('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)
        self._close_channel()

    # Setup
    def _open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """
        logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self._on_channel_open)

    def _add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(self._on_channel_closed)

    def _setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.
        :param str|unicode exchange_name: The name of the exchange to declare
        """
        logger.info('Declaring exchange: %s', exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(
            self._on_exchange_declareok, userdata=exchange_name)
        self._channel.exchange_declare(
            durable=True,
            exchange=exchange_name,
            exchange_type=ExchangeType.direct,
            callback=cb)

    def _setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        :param str|unicode queue_name: The name of the queue to declare.
        """
        logger.info('Declaring queue %s', queue_name)
        cb = functools.partial(self._on_queue_declareok, userdata=queue_name)

        self._channel.queue_declare(queue=queue_name, durable=True,
                                    arguments={"x-queue-type": "quorum"},
                                    callback=cb)

    def _setup_delay_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        :param str|unicode queue_name: The name of the queue to declare.
        """
        logger.info('Declaring delay queue %s', queue_name)
        self._declare_delay_queue(queue_name)

    def _setup_error_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        :param str|unicode queue_name: The name of the queue to declare.
        """
        logger.info('Declaring error queue %s', queue_name)
        self._declare_error_queue(queue_name)

    def _declare_delay_queue(self, queue_name):
        self._channel.queue_declare(queue=queue_name, durable=True,
                                    arguments={"x-queue-type": "classic",
                                               "x-message-ttl": self.config.requeue_message_delay,
                                               "x-dead-letter-exchange": self.config.exchange,
                                               "x-dead-letter-routing-key": self.config.routing_key})

    def _declare_error_queue(self, queue_name):
        self._channel.queue_declare(queue=queue_name, durable=True,
                                    arguments={"x-queue-type": "quorum"})

    def _set_qos(self):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.
        """
        self._channel.basic_qos(
            prefetch_count=self.config.prefetch_count,
            callback=self._on_basic_qos_ok)

    def _start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """
        logger.info('Issuing consumer related RPC commands')
        self._add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.config.queue, self._on_message)
        self._consuming = True

    def _add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.
        """
        logger.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self._on_consumer_cancelled)

    def _stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._channel:
            logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self._on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    # Lifecycle management
    def run(self):
        """Run the consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """
        self._connection = self._connect()
        self._connection.ioloop.start()

    def stop(self):
        """
        This is an asynchronous method to stop the current thread. It is thread safe and can be called from any thread.
        It works by scheduling a shutdown callback using the running event loop.
        """
        self._connection.ioloop.add_callback_threadsafe(self._shutdown)

    def _reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        if self._reconnect_counter >= self.config.connection_retry_limit:
            logger.error("Reached reconnect limit. Aborting consumer.")
            self._shutdown()
        else:
            self._reconnect_counter += 1
            time.sleep(self.config.connection_retry_wait)
            logger.info(f"Reconnect, attempt {self._reconnect_counter}")
            self._connection.ioloop.stop()
            self.run()

    def _shutdown(self):
        """The actual shutdown method. This method marks the thread as closing, and proceeds to close
        the channel & connection, and finally the event loop itself."""
        logger.info("Stopping consumer")
        self._closing = True
        self._close_channel()
        self._close_connection()
        self._connection.ioloop.stop()
        logger.info("Stopped consumer")

    def _close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        logger.info('Closing the channel')
        if self._channel is not None and self._channel.is_open:
            self._channel.close()

    def _close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            logger.info('Connection is closing or already closed')
        else:
            logger.info('Closing connection')
            self._connection.close()

    # Normal run methods
    def _run_message_callback(self, delivery_tag, body, properties):
        try:

            logger.info('Received message # %s: %s', delivery_tag, body)
            self._on_consumption_callback(body)
            logger.info('Adding acknowledge callback %s', delivery_tag)
            cb = functools.partial(self._acknowledge_message, delivery_tag)
            self._connection.ioloop.add_callback_threadsafe(cb)
        except BaseDeterministicError:
            logger.info('Deterministic error on message: # %s', delivery_tag)
            logger.info('Adding reject callback # %s', delivery_tag)
            logger.info('Rejecting message # %s', delivery_tag)
            cb = functools.partial(self._reject_message, delivery_tag, False, body)
            self._connection.ioloop.add_callback_threadsafe(cb)
        except BaseEnvironmentalError:
            logger.info('Environmental error on message: # %s', delivery_tag)
            logger.info('Adding unacknowledge callback %s', delivery_tag)
            cb = functools.partial(self._reject_message, delivery_tag, True, body)
            self._connection.ioloop.add_callback_threadsafe(cb)
        except BaseUnknownError:
            logger.info('Unknown error on message: # %s', delivery_tag)
            logger.info('Adding unacknowledge callback %s', delivery_tag)
            cb = functools.partial(self._reject_message, delivery_tag, True, body, properties, True)
            self._connection.ioloop.add_callback_threadsafe(cb)

    def _acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.
        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        """
        logger.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def _reject_message(self, delivery_tag, requeue: bool, body=None, properties=None, limit_retries=False):
        """Reject the message delivery from RabbitMQ by sending a
        Basic.Reject RPC method for the delivery tag.
        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.
        """
        if requeue:
            if limit_retries:
                counter = properties.headers.get('delivery-counter')
                if counter is None:
                    counter = 1
                else:
                    counter += 1

                if counter > self.config.requeue_message_max_tries:
                    logger.info('Rejecting message %s as counter reached max retries', delivery_tag)
                    logger.info('Message %s rejected and visible in %s queue', delivery_tag,
                                self.config.error_queue_name)
                    self._channel.basic_reject(delivery_tag, requeue=False)
                    self._channel.basic_publish(routing_key=self.config.delay_queue,
                                                body=body,
                                                exchange=""
                                                )
                else:
                    logger.info('Requeuing message # %s', delivery_tag)
                    logger.info('Retrying message %s, attempt %s/%s', delivery_tag,
                                counter, self.config.requeue_message_max_tries)
                    props = pika.BasicProperties(delivery_mode=2, headers={'delivery-counter': counter})
                    self._channel.basic_reject(delivery_tag, requeue=False)
                    self._channel.basic_publish(routing_key=self.config.delay_queue,
                                                body=body,
                                                properties=props,
                                                exchange=""
                                                )
            else:
                logger.info('Requeuing message # %s', delivery_tag)
                props = pika.BasicProperties(delivery_mode=2)
                self._channel.basic_reject(delivery_tag, requeue=False)
                self._channel.basic_publish(routing_key=self.config.delay_queue,
                                            body=body,
                                            properties=props,
                                            exchange=""
                                            )
        else:
            logger.info('Message %s rejected and visible in %s queue', delivery_tag,
                        self.config.error_queue_name)
            self._channel.basic_reject(delivery_tag, requeue=requeue)
            self._channel.basic_publish(routing_key=self.config.error_queue_name,
                                        body=body,
                                        exchange=""
                                        )
