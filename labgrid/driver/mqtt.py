#!/usr/bin/env python3

from calendar import c
import time

import attr

from .common import Driver
from ..factory import target_factory
from ..protocol import LEDProtocol
from ..step import step
from ..util import Timeout


class MQTTError(Exception):
    pass

@target_factory.reg_driver
@attr.s(eq=False)
class MQTTDriver(Driver):
    bindings = {
            "mqtt": {"MQTTResource"}
    }
    subscribed_topic = ""
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        import paho.mqtt.client as mqtt
        self._client = mqtt.Client()
        
    def on_activate(self):
        print(f"<driver> mqtt driver active")
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self.mqtt.host)
        self._client.loop_start()
        
    def _on_connect(self, client, userdata, flags, rc):
        if(self.subscribed_topic != ""):
            self._client.subscribe(self.subscribed_topic)
        print(f"<driver> mqtt client connected")

    def _on_message(self, client, userdata, msg):
        print(f"<driver> topic: {msg.topic} payload: {msg.payload}")
        self.payload = msg.payload

@target_factory.reg_driver
@attr.s(eq=False)
class LEDBoardTopicDriver(Driver):
    bindings = {
            "board": {"LEDBoardTopic"}
    }
    subscribed_topics = []
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        import paho.mqtt.client as mqtt
        self._client = mqtt.Client()
        
    def on_activate(self):
        print(f"<driver> mqtt driver active")
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self.board.host)
        self._client.loop_start()
        
    def _on_connect(self, client, userdata, flags, rc):
        for i in self.subscribed_topics:
            if(i != ""):
                self._client.subscribe(self.board.board_topic + "/" + i)
                print("subscribe to " + self.board.board_topic + "/" + i)
            else:
                self._client.subscribe(self.board.board_topic + "/#")
                print("subscribe to " + self.board.board_topic)
        print(f"<driver> mqtt client connected")

    def _on_message(self, client, userdata, msg):
        print(f"<driver> topic: {msg.topic} payload: {msg.payload}")
        self.payload = msg.payload


#old
@target_factory.reg_driver
@attr.s(eq=False)
class LEDDetTopicDriver(Driver, LEDProtocol):
    bindings = {
            "led": {"LEDDetTopics"}
    }
    _client = attr.ib(default=None)
    _status = attr.ib(default=None)
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        import paho.mqtt.client as mqtt
        self._client = mqtt.Client()

    def on_activate(self):
        print(f"<driver> mqtt driver active")
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self.led.host)
        self._client.loop_start()
        
    def on_deactivate(self):
        print(f"<driver> stop mqtt client loop")
        self._client.loop_stop()
    
    def _on_connect(self, client, userdata, flags, rc):
        self._client.subscribe(self.led.avail_topic)
        print(f"<driver> mqtt client connected")

    
    def _on_message(self, client, userdata, msg):
        print(f"<driver> topic: {msg.topic} payload: {msg.payload}")
        self.payload = msg.payload

    @Driver.check_active
    @step()
    def random(self):
        print(f"<driver> mqtt subscribe to random topic")
        self._client.subscribe(self.led.random_topic)
    
    @Driver.check_active
    @step()
    def joke(self):
        print(f"<driver> mqtt subscribe to joke topic")
        self._client.subscribe(self.led.joke_topic)
        