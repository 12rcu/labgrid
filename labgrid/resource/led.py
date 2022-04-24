import logging

import attr

from .common import ManagedResource, ResourceManager
from ..factory import target_factory


@attr.s(eq=False)
class LedDetection(ManagedResource):
    host = attr.ib(validator=attr.validators.instance_of(str))
    mqtt_port = attr.ib(validator=attr.validators.instance_of(str))
    reference = attr.ib(validator=attr.validators.instance_of(str))
    webcam_id = attr.ib(validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
