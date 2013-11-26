# -*- coding: utf-8 -*-
###############################################################################
# Name: language.py
# Purpose: MoRP Language support.
# Languages consists of abstract syntax, zero or mode concrete syntaxes given
# in the form of editor configuration and zero or more semantics definition 
# given in the form of generator configuration.
# 
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

from morpy.core import NamedElement
from morpy.const import MORP

class Language(NamedElement):
    '''
    Represents a MoRP language.
    
    Attributes:
        name(string):
        abstract_syntax(Mogram): An language abstract syntax given in MoRP language.
        concrete_syntaxes(list of Mogram): Defines concrete syntaxes in the form of 
                editor configuration mograms.
        generators(list of Mogram): Defines a language semantics in the form of 
                generator configuration mograms.
    '''
    
    def __init__(self, name, abssyn_uuid=None, **kwargs):
        from morpy import repository
        super(Language, self).__init__(name=name, meta=repository.model, **kwargs)
        
        # Special case. If this instance represents MoRP language its
        # abstract syntax is defined in this language.
        # This must be specified in this way because MoRP language is 
        # not defined at this point yet. 
        if name=='MoRP':
            abssyn_language = self
        else:
            # Currently the only language for abstract syntax definition is MoRP
            abssyn_language = repository.morp
            
        self.abstract_syntax = Mogram(name, conforms_to=abssyn_language, 
                                      language=self, uuid=abssyn_uuid)
        self.concrete_syntaxes = []
        self.generators = []
        

class Mogram(NamedElement):
    '''
    Represents a mogram given in some language.
    
    Attributes:
        content (list): A list of Model instances.
        conforms_to (Mogram): An abstract syntax of the language this mogram conforms to.
        language (Language): If this mogram is part of some language definition this reference
                will contain instance of containing Language.
    '''
    def __init__(self, name, conforms_to, language=None, **kwargs):
        from morpy import repository
        super(Mogram, self).__init__(name=name, meta=repository.model, **kwargs)
        
        self.contents = []
        if not conforms_to and name==MORP:
            # MoRP conforms to its own abstract syntax
            self.conforms_to = self
        else:
            self.conforms_to = conforms_to
        self.language = language
        
    def add_model(self, model):
        self.contents.append(model)
        
    def __iter__(self):
        return iter(self.contents)
    
    def __contains__(self, model):
        return model in self.contents


    
        