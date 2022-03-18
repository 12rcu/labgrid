import logging
import threading
from time import monotonic

import attr

from .common import ManagedResource, ResourceManager
from ..factory import target_factory

@attr.s(eq=False)
class MQTTManager(ResourceManager):
    _available = attr.ib(default=attr.Factory(set), validator=attr.validators.instance_of(set))
    _avail_lock = attr.ib(default=threading.Lock())
    _clients = attr.ib(default=attr.Factory(dict), validator=attr.validators.instance_of(dict))
    _topics = attr.ib(default=attr.Factory(list), validator=attr.validators.instance_of(list))
    _topic_lock = attr.ib(default=threading.Lock())
    _last = attr.ib(default=0.0, validator=attr.validators.instance_of(float))

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.log = logging.getLogger('MQTTManager')

    def _create_mqtt_connection(self, host):
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect(host)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.loop_start()
        return client

    def on_resource_added(self, resource):
        host = resource.host
        if host not in self._clients:
            self._clients[host] = self._create_mqtt_connection(host)
        self._clients[host].subscribe(resource.avail_topic)

    def _on_message(self, client, userdata, msg):
        # print(f"<resource> mqtt message in topic {msg.topic} received with payload: {msg.payload.decode('utf-8')}")
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        
        with self._avail_lock:
                self._available.add(topic)
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("<resource> Connected to MQTT Broker!")
        else:
            print("<resource> Failed to connect, return code %d\n", rc)
        
        #client.subscribe("$SYS/#")


    def poll(self):
        if monotonic()-self._last < 2:
            return  # ratelimit requests
        self._last = monotonic()
        with self._avail_lock:
            for resource in self.resources:
                resource.avail = resource.avail_topic in self._available


@target_factory.reg_resource
@attr.s(eq=False)
class MQTTResource(ManagedResource):
    manager_cls = MQTTManager

    host = attr.ib(validator=attr.validators.instance_of(str))
    avail_topic = attr.ib(validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        self.timeout = 120.0
        super().__attrs_post_init__()


@target_factory.reg_resource
@attr.s(eq=False)
class TasmotaPowerPort(MQTTResource):
    power_topic = attr.ib(default=None,
                         validator=attr.validators.instance_of(str))
    status_topic = attr.ib(default=None,
                         validator=attr.validators.instance_of(str))
    

# old
@target_factory.reg_resource
@attr.s(eq=False)
class LEDDetTopics(MQTTResource):
    random_topic = attr.ib(default=None,
                         validator=attr.validators.instance_of(str))
    joke_topic = attr.ib(default=None,
                         validator=attr.validators.instance_of(str))

@target_factory.reg_resource
@attr.s(eq=False)
class LEDBoardTopic(MQTTResource):
    board_topic = attr.ib(default=None, validator=attr.validators.instance_of(str))