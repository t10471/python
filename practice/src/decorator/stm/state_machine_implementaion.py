# -*- coding: utf-8 -*-

# State Machine example Program

from statedefn import *
import traceback

class MyMachine(object):

    # Create Statedefn object for each state you need to keep track of.
    # the name passed to the constructor becomes a StateVar member of the current class.
    # i.e. if my_obj is a MyMachine object, my_obj.gstate maintains the current gstate
    gstate = StateTable("gstate")
    tstate = StateTable("turtle")

    def __init__(self, name):
        # must call init method of class's StateTable object. to initialize state variable
        self.gstate.initialize(self)
        self.tstate.initialize(self)
        self.mname = name
        self.a_count = 0
        self.b_count = 0
        self.c_count = 0

    # Decorate the Event Handler virtual functions -note gstate parameter
    #この関数自体は処理を書いても実行されない
    @event_handler(gstate)
    def event_a(self): pass
    @event_handler(gstate)
    def event_b(self): pass
    @event_handler(gstate)
    def event_c(self, val): pass

    @event_handler(tstate)
    def toggle(self): pass


    # define methods to handle events.
    def _event_a_hdlr1(self):
        print "State 1, event A"
        self.a_count += 1
    def _event_b_hdlr1(self):
        print "State 1, event B"
        self.b_count += 1
    def _event_c_hdlr1(self, val):
        print "State 1, event C"
        self.c_count += 3*val

    def _event_a_hdlr2(self):
        print "State 2, event A"
        self.a_count += 10
        # here we brute force the tstate to on, leave & enter functions called if state changes.
        # turtle is object's state variable for tstate, comes from constructor argument
        #gstateの処理中にtstateの状態を変更する
        self.turtle.set_state(self, self._t_on)
    def _event_b_hdlr2(self):
        print "State 2, event B"
        self.b_count += 10
    def _event_c_hdlr2(self, val):
        print "State 2, event C"
        self.c_count += 2*val

    def _event_a_hdlr3(self):
        self.a_count += 100
        print "State 3, event A"
    def _event_b_hdlr3(self):
        print "State 3, event B"
        self.b_count += 100
        # we decide here we want to go to state 2, overrrides spec in state table below.
        # transition to next_state is made after the method exits.
        self.gstate.next_state = self._state2
    def _event_c_hdlr3(self, val):
        print "State 3, event C"
        self.c_count += 5*val

    # Associate the handlers with a state. The first argument is a list of methods.
    # One method for each event_handler decorated function of gstate. Order of methods
    # in the list correspond to order in which the Event Handlers were declared.
    # Second arg is the name of the state.  Third argument is to be come a list of the
    # next states.
    # The first state created becomes the initial state.
    #状態と処理の紐付けを行う
    _state1 = gstate.state("One",  (_event_a_hdlr1, _event_b_hdlr1, _event_c_hdlr1),
                                      ("Two", "Three", None))
    _state2 = gstate.state("Two",  (_event_a_hdlr2, _event_b_hdlr2, _event_c_hdlr2),
                                     ("Three",        None,          "One"))
    _state3 = gstate.state("Three",(_event_a_hdlr3, _event_b_hdlr3, _event_c_hdlr3),
                                 (None,         "One",         "Two"))


    # Declare a function that will be called when entering a new gstate.
    # Can also declare a leave function using @on_leave_function(gstate)
    @on_enter_function(gstate)
    def _enter_gstate(self):
        print "entering state ", self.gstate.name() , "of ", self.mname
    @on_leave_function(tstate)
    def _leave_tstate(self):
        print "leaving state ", self.turtle.name() , "of ", self.mname


    def _toggle_on(self):
        print "Toggle On"

    def _toggle_off(self):
        print "Toggle Off"

    _t_off = tstate.state("Off", [_toggle_on],
                         ["On"])
    _t_on =  tstate.state("On", [_toggle_off],
                          ["Off"])


def main():
    big_machine = MyMachine("big")
#    lil_machine = MyMachine("lil")
    print "event_a"
    big_machine.event_a()
#    lil_machine.event_a()
    print "event_a"
    big_machine.event_a()
#    lil_machine.event_a()
    print "event_b"
    big_machine.event_b()
#    lil_machine.event_b()
    print "event_c"
    big_machine.event_c(4)
#    lil_machine.event_c(2)
    print "event_c"
    big_machine.event_c(1)
#    lil_machine.event_c(3)
    print "event_b"
    big_machine.event_b()
#    lil_machine.event_b()
    print "event_a"
    big_machine.event_a()
#    lil_machine.event_a()
    print "event_a"
    big_machine.event_a()

    print "toggle"
    big_machine.toggle()
    print "toggle"
    big_machine.toggle()
    print "toggle"
    big_machine.toggle()

#    lil_machine.event_a()
    print "event_b"
    big_machine.event_b()
#    lil_machine.event_b()
    print "event_c"
    big_machine.event_c(3)
    print "event_a"
    big_machine.event_a()
#    lil_machine.event_c(2)
#    lil_machine.event_a()
    print "event_b"
    big_machine.event_b()
#    lil_machine.event_b()
    print "event_c"
    big_machine.event_c(7)
#    lil_machine.event_c(1)

    print "Event A count ", big_machine.a_count
    print "Event B count ", big_machine.b_count
    print "Event C count ", big_machine.c_count
#    print "LilMachine C count ", lil_machine.c_count

main()