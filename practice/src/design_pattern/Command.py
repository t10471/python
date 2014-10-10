# -*- coding: utf-8 -*-

#大体chain of responseibilityと同じだが、
#chain of responseibilityはhandlerと実処理が一緒なのに対して
#commandはhandlerと実処理が別になっている

class File(object):

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def decompress(self):
        print self.name + u'を展開しました'

    def compress(self):
        print self.name + u'を圧縮しました'

    def create(self):
        print self.name + u'を作成しました'

class TouchCommand(object):

    def __init__(self, file):
        self.file = file

    def execute(self):
        self.file.create()

class CompressCommand (object):

    def __init__(self, file):
        self.file = file

    def execute(self):
        self.file.compress()

class CopyCommand(object):

    def __init__(self, file):
        self.file = file

    def execute(self):
        file = File('copy ' + self.file.getName())
        file.create()


class Queue(object):
    def __init__(self):
        self.commands = []
        self.current_index = 0

    def addCommand(self, command):
        self.commands.append(command)

    def run(self):
        while True:
            command = self.next()
            if command is None:
                break
            command.execute()

    def next(self):
        if len(self.commands) == 0 or len(self.commands) <= self.current_index:
            return None
        else:
            ret =  self.commands[self.current_index]
            self.current_index = self.current_index + 1
            return ret

if __name__ == '__main__':
    queue = Queue()
    file = File("sample.txt")
    queue.addCommand(TouchCommand(file))
    queue.addCommand(CompressCommand(file))
    queue.addCommand(CopyCommand(file))

    queue.run()