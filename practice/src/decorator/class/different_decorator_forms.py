# -*- coding: utf-8 -*-

from sys import stdout,stderr
from pdb import set_trace as bp
import traceback

class DecoTrace(object):
    '''
    Decorator class with no arguments
    This can only be used for functions or methods where the instance
    is not necessary
    '''

    def __init__(self, f):
        self.f = f
        print self.f.__name__, self.__class__.__name__, traceback.extract_stack()[-1][2]

    def _showargs(self, *fargs, **kw):
        print >> stderr, 'T: enter %s with args=%s, kw=%s' % (self.f.__name__, str(fargs), str(kw))

    def _aftercall(self, status):
        print >> stderr, 'T: exit %s with status=%s' % (self.f.__name__, str(status))

    def __call__(self, *fargs, **kw):
        '''pass just function arguments to wrapped function'''
        print self.f.__name__, self.__class__.__name__, traceback.extract_stack()[-1][2]
        self._showargs(*fargs, **kw)
        ret=self.f(*fargs, **kw)
        self._aftercall(ret)
        return ret

    def __repr__(self):
        return self.f.func_name


class DecoTraceWithArgs(object):
    '''decorator class with ARGUMENTS
       This can be used for unbounded functions and methods.  If this wraps a
       class instance, then extract it and pass to the wrapped method as the
       first arg.
    '''

    def __init__(self, *dec_args, **dec_kw):
        '''The decorator arguments are passed here.  Save them for runtime.'''
        print self.__class__.__name__, traceback.extract_stack()[-1][2]
        self.dec_args = dec_args
        self.dec_kw = dec_kw

        self.label = dec_kw.get('label', 'T')
        #print self.label
        #出力ストリーム
        self.fid = dec_kw.get('stream', stderr)
        #print self.fid

    def _showargs(self, *fargs, **kw):

        print >> self.fid, \
              '%s: enter %s with args=%s, kw=%s' % (self.label, self.f.__name__, str(fargs), str(kw))
        print >> self.fid, \
              '%s:   passing decorator args=%s, kw=%s' % (self.label, str(self.dec_args), str(self.dec_kw))

    def _aftercall(self, status):
        print >> self.fid, '%s: exit %s with status=%s' % (self.label, self.f.__name__, str(status))
    def _showinstance(self, instance):
        print >> self.fid, '%s: instance=%s' % (self.label, instance)

    def __call__(self, f):
        print f.__name__, self.__class__.__name__, traceback.extract_stack()[-1][2]
        def wrapper(*fargs, **kw):
            '''
              Combine decorator arguments and function arguments and pass to wrapped
              class instance-aware function/method.
              Note: the first argument cannot be "self" because we get a parse error
              "takes at least 1 argument" unless the instance is actually included in
              the argument list, which is redundant.  If this wraps a class instance,
              the "self" will be the first argument.
            '''
            print f.__name__, self.__class__.__name__, traceback.extract_stack()[-1][2]
            self._showargs(*fargs, **kw)

            # merge decorator keywords into the kw argument list
            kw.update(self.dec_kw)

            # Does this wrap a class instance?
            #if fargs and getattr(fargs[0], '__class__', None):
            #インスタンスかどうかの判定
            if fargs and str(type(fargs[0])).split("'")[0].strip("< ") == "class":

                print True
                # pull out the instance and combine function and
                # decorator args
                instance, fargs = fargs[0], fargs[1:]+self.dec_args
                self._showinstance(instance)

                # call the method
                ret=f(instance, *fargs, **kw)
            else:
                print False
                # just send in the give args and kw
                ret=f(*(fargs + self.dec_args), **kw)

            self._aftercall(ret)
            return ret

        # Save wrapped function reference
        self.f = f
        wrapper.__name__ = f.__name__
        wrapper.__dict__.update(f.__dict__)
        wrapper.__doc__ = f.__doc__
        return wrapper


@DecoTrace
def FirstBruce(*fargs, **kwargs):
    'Simple function using simple decorator'
    if fargs and fargs[0]:
        print fargs[0]

@DecoTraceWithArgs(name="Second Bruce", standardline="Goodday, Bruce!")
def SecondBruce(*fargs, **kwargs):
    'Simple function using decorator with arguments'
    print '%s:' % kwargs.get('name', 'Unknown Bruce'),

    if fargs and fargs[0]:
        print fargs[0]
    else:
        print kwargs.get('standardline', None)

class Bruce(object):
    'Simple class'

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self):
        return 'Bruce'

    @DecoTraceWithArgs(label="Trace a class", standardline="How are yer Bruce?", stream=stdout)
    def talk(self, *fargs, **kwargs):
        'Simple function using decorator with arguments'
        print "self", self
        self.test()
        print '%s:' % self,
        if fargs and fargs[0]:
            print fargs[0]
        else:
            print kwargs.get('standardline', None)
    def test(self):
        print "test"

#DecoTraceの__call__はここで呼ばれる
print "DecoTrace FirstBruce start"
FirstBruce("First Bruce: Oh, Hello Bruce!")
print "DecoTrace FirstBruce end"

#DecoTraceWithArgsの__call__はここで呼ばれず、宣言時に呼ばれるここではwrapperが呼ばれる
print "DecoTraceWithArgs SecondBruce start"
SecondBruce("That's a strange expression, Bruce.")
print "DecoTraceWithArgs SecondBruce end"

ThirdBruce = Bruce('Third Bruce')

print "DecoTraceWithArgs ThirdBruce start"
print ThirdBruce
ThirdBruce.talk()
print "DecoTraceWithArgs ThirdBruce end"

#
#SecondBruce()
#FirstBruce("First Bruce: Oh, Hello Bruce!")
#ThirdBruce.talk()
#FirstBruce("First Bruce: Bit crook, Bruce.")
#SecondBruce("Where's Bruce?")
#FirstBruce("First Bruce: He's not here, Bruce")
#ThirdBruce.talk("Blimey, s'hot in here, Bruce.")
#FirstBruce("First Bruce: S'hot enough to boil a monkey's bum!")
#SecondBruce("That's a strange expression, Bruce.")
#FirstBruce("First Bruce: Well Bruce, I heard the Prime Minister use it.S'hot enough to boil a monkey's bum in 'ere, your Majesty,' he said and she smiled quietly to herself.")
#ThirdBruce.talk("She's a good Sheila, Bruce and not at all stuck up.")