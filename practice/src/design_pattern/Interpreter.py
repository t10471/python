# -*- coding: utf-8 -*-
import datetime
import os

#compsiteとcommandをあわせたような形
#ContextがhandlerでCommandが処理

class JobCommand(object):
    def execute(self, context):
        if context.getCurrentCommand() != 'begin':
            raise Exception('illegal command ' + str(context.getCurrentCommand()))

        command_list = CommandListCommand()
        command_list.execute(context.next())



class CommandListCommand(object):
    def execute(self, context):
        while (True):
            current_command = context.getCurrentCommand()
            if current_command is None:
                raise Exception('"end" not found ')
            elif current_command == 'end':
                break
            else:
                command = CommandCommand()
                command.execute(context)

            context.next()


class CommandCommand(object):
    def execute(self, context):
        current_command = context.getCurrentCommand()
        if current_command == 'diskspace':
            free_size = 100000000.0
            max_size  = 210000000.0
            ratio = free_size / max_size * 100

            print( 'Disk Free : %dMB (%.2f%%)' % (free_size / 1024 / 1024, ratio))
        elif current_command == 'date':
            print datetime.datetime.today().strftime("%Y/%m/%d")
        elif current_command == 'line':
            print '--------------------'
        else:
            raise Exception('invalid command [' + str(current_command) + ']')

class Context(object):
    def __init__(self, command):
        self.commands = []
        self.current_index = 0
        self.max_index = 0
        self.commands = command.strip().split()
        print self.commands
        self.max_index = len(self.commands)


    def next(self):
        self.current_index += 1
        print self.current_index
        return self


    def getCurrentCommand(self):
        if self.current_index > len(self.commands):
            return None
        return self.commands[self.current_index].strip()


def execute(command):
    job = JobCommand()
    try:
        job.execute(Context(command))
    except Exception, e:
        print e.args



if __name__ == '__main__':

    command = 'begin date line diskspace end'
    if command != '':
        execute(command)

