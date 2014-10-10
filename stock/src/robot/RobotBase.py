#*- coding: utf-8 -*-

from model.connection import get_session

class RobotBase(object):
    def __init__(self):
        self.connection = get_session()

    def run(self):
        self._run()

    def _run(self):
        pass