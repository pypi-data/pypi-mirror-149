"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from dataclasses import dataclass
from .server import Response, Server
from typing import Any


@dataclass
class IArgs:
    server:Server
    response:Response
    config:Any


class FunctionUnit:
    """Functional block
    """
    static:IArgs = None

    @staticmethod
    def init(server=None, response=None, config=None):
        FunctionUnit.static = IArgs(server, response, config)

    @staticmethod
    def start(*args, **kwargs):
        FunctionUnit.init(*args, **kwargs)

    @staticmethod
    def clear_static():
        FunctionUnit.init()

    @staticmethod
    def end():
        FunctionUnit.init()

    def __init__(self, func):
        self.func = func

    def run(self):
        response = self.func(FunctionUnit)
        FunctionUnit.static.response = response

    def __call__(self, *args, **kwargs):
        self.run()


