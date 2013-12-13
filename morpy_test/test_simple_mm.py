#-*- coding: utf-8 -*-
###############################################################################
# Name: test_morp.py
# Purpose: Testing simple meta-model instantiation.
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

import unittest
from morpy import Workspace

class SimpleMMTest(unittest.TestCase):
            
    def test_01_language_create(self):
        lang = Workspace().create_language("Simple")
        self.assertIn(lang.name, Workspace())
        
    def test_02_create_abstract_syntax(self):
        lang = Workspace().languages['Simple']
        asyn = lang.abstract_syntax
        
        # Create Class model
        cls = asyn.create_model("Class")
        self.assertIn("Class", asyn)
        self.assertIn(cls, asyn)
        
        # Create Attribute model
        attr = asyn.create_model("Attribute")
        self.assertIn("Attribute", asyn)
        self.assertIn(attr, asyn)        
    
    def test_03_instantiate_model(self):
        '''
        Tests that model can be instantiated.
        '''
        mogram = Workspace().create_mogram('Gate', 'MoRP')
        mogram.create_model('Machine')
        
