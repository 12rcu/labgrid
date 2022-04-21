import logging

import attr

from .common import ManagedResource, ResourceManager
from ..factory import target_factory

@attr.s(eq=False)
class LedDetection(ResourceManager):
    _clients = attr.ib(default=attr.Factory(dict), validator=attr.validators.instance_of(dict))
    
    def __attrs_post_init__(self):
        super().__attrs_post_init__()
    
