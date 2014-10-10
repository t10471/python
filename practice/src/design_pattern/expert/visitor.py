# -*- coding: utf-8 -*-

class vlist(list):
    def accept(self, visitor):
        visitor.visit_list(self)

class vdict(dict):
    def accept(self, visitor):
        visitor.visit_dict(self)

class Printer(object):
    def visit_list(self, ob):
        print 'list content :'
        print str(ob)

    def visit_dict(self, ob):
        print 'dict keys: %s' % ','.join(ob.keys())

a_list = vlist([1,2,5])
a_list.accept(Printer())

a_dict = vdict({'one':1, 'two':2, 'three':3})
a_dict.accept(Printer())

def visit(visited, visitor):
    cls = visited.__class__.__name__
    meth = 'visit_%s' % cls
    method = getattr(visitor, meth, None)
    if method is not None:
        method(visited)

visit([1,2,5], Printer())
visit({'one':1, 'two':2, 'three':3}, Printer())

import os
def visit_dir(directory, visitor):
    for root, dirs, files in os.walk(directory):
        for f in files:
            #foo.txt -> txt
            print f
            print os.path.splitext(f)[-1]
            ext = os.path.splitext(f)[-1][1:]
            meth = getattr(visitor, ext, None)
            if meth is not None:
                meth(os.path.join(root, f))

class FileReader(object):
    def pdf(self, f):
        print 'processing %s' % f
    def py(self, f):
        print 'python %s' % f


visit_dir('.', FileReader())