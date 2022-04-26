#!/usr/bin/env python3
import subprocess

import attr

from .common import Driver
from ..factory import target_factory


@target_factory.reg_driver
@attr.s(eq=False)
class LedDetDriver(Driver):
    bindings = {
            "led": {"LedDetection"}
    }
    video = False
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
    
    def on_activate(self):
        arg = "/root/leddet/LED-Detection/src/manin.py "
        if self.led.host is not None:
            arg += "-bh " + self.led.host + " "
        if self.led.mqtt_port is not None: 
            arg += "-bp " + self.led.mqtt_port + " "
        if self.led.reference is not None:
            arg += "-r " + self.led.reference + " "
        if self.led.webcam_id is not None:
            arg += "-w " + self.led.webcam_id + " "
        if self.video:
            arg += "-v "

        subprocess.Popen(
            arg
        )
    
    @Driver.check_active
    def stream(self):
        pipeline = [
            "gst-launch-1.0",
            "souphttpsrc",
            f"location=127.0.0.1:8000",
            "!",
            "decodebin",
            "!",
            "autovideoconvert",
            "!",
            "autovideosink",
            "sync=false",
        ]

        subprocess.run(pipeline)