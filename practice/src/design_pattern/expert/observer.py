# -*- coding: utf-8 -*-

class Event(object):
    _observers = []
    def __init__(self, subject):
        self.subject = subject

    @classmethod
    def register(cls, observer):
        if observer not in cls._observers:
            cls._observers.append(observer)

    @classmethod
    def unregister(cls, observer):
        if observer in cls._observers:
            cls._observers.remove(observer)

    @classmethod
    def notify(cls, subject):
        event = cls(subject)
        for observer in cls._observers:
            observer(event)

class WriteEvent(Event):
    _observers = []
    def __repr__(self):
        return 'WriteEvent'

def log(event):
    print '%s was written' % event.subject

WriteEvent.register(log)

class AnotherObserver(object):
    def __call__(self, event):
        print 'Yeah %s told me !' % event

WriteEvent.register(AnotherObserver())

WriteEvent.notify('a given file')