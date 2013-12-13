#-*- coding: utf-8 -*-
#######################################################################
# Name: exceptions.py
# Purpose: MoRP exceptions
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#######################################################################

class MoRPyException(Exception):
    '''
    Root of MoRPy exception hierarchy.
    '''
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message
    
    
class LanguageExists(MoRPyException):
    '''
    Raised if caller tries to create new language with the name
    that is already registered in the repository.
    '''
    def __init__(self, name):
        super(LanguageExists, self).__init__(\
                    "Language with the name '%s' is already registered." % name)
        
class MogramExists(MoRPyException):
    '''
    Raised if caller tries to create new mogram with the name
    that is already registered in the repository.
    '''
    def __init__(self, name):
        super(MogramExists, self).__init__(\
                    "Mogram with the name '%s' is already registered." % name)        