#!/usr/bin/env python3

from calendar import c
import time

import attr

from .common import Driver
from ..factory import target_factory
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
        if self.subscribed_topic != "":
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
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect(self.board.host)
        self._client.loop_start()
        
    def _on_connect(self, client, userdata, flags, rc):
        print(f"<mqtt-driver> mqtt client connected")
        for i in self.subscribed_topics:
            # i.removePrefix("/")
            if i != "all":
                self._client.subscribe(self.board.board_topic + "/" + i)
                print("<mqtt-driver> subscribe to " + self.board.board_topic + "/" + i)
            else:
                self._client.subscribe(self.board.board_topic + "/#")
                print("<mqtt-driver> subscribe to " + self.board.board_topic + "/#")

    def _on_message(self, client, userdata, msg):
        print(f"<mqtt-driver> topic: {msg.topic} payload: {msg.payload}")
        self.payload = msg.payload
