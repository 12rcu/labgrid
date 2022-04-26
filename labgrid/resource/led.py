import attr

from .common import Resource
from ..factory import target_factory


@target_factory.reg_resource
@attr.s(eq=False)
class LedDetection(Resource):
    host = attr.ib(validator=attr.validators.instance_of(str))
    mqtt_port = attr.ib(validator=attr.validators.instance_of(str))
    reference = attr.ib(validator=attr.validators.instance_of(str))
    webcam_id = attr.ib(validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
