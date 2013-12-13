#-*- coding: utf-8 -*-
###############################################################################
# Name: test_morp.py
# Purpose: Testing MoRP core concepts.
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

import unittest
from morpy import MoRPRepository
from morpy.const import NAMED_ELEMENT, MULTIPLICITY, MODEL, REFERENCE, PROPERTY,\
    PRIMITIVE_TYPES, PRIMITIVE_TYPES_PRIMITIVE_TYPE, PRIMITIVE_TYPES_BOOLEAN,\
    PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING, LANGUAGE, MOGRAM

morp_toplevel_model_names = [LANGUAGE, MOGRAM, NAMED_ELEMENT, MULTIPLICITY, MODEL,\
                              REFERENCE, PROPERTY, PRIMITIVE_TYPES]
primitive_type_models = [PRIMITIVE_TYPES_PRIMITIVE_TYPE, PRIMITIVE_TYPES_BOOLEAN, \
                         PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING]

class MoRPTest(unittest.TestCase):
    
    def setUp(self):
        '''
        Clear singleton instance attribute to force reinitialization. 
        '''
        try:
            delattr(MoRPRepository, "_instance")
        except:
            pass
    
    def test_MoRP_models(self):
        '''
        Tests MoRP models.
        '''
        
        # Top-level abstract models
        abstract_models = filter(lambda m: m.abstract, MoRPRepository().morp)
        abstract_model_names = [x.name for x in abstract_models]

        self.assertItemsEqual(abstract_model_names, [NAMED_ELEMENT, MULTIPLICITY])
        
        # Top-level models
        toplevel_model_names = [x.name for x in MoRPRepository().morp]
        self.assertItemsEqual(toplevel_model_names, morp_toplevel_model_names)
        
    def test_model_iteration(self):
        '''
        Test that model iteration returns inner models.
        '''
        
        for model in MoRPRepository().morp:
            self.assertIn(model.name, morp_toplevel_model_names)
            if model.name == PRIMITIVE_TYPES:
                primitive_types = model
            
        for model in primitive_types:
            self.assertIn(model.name, primitive_type_models)
            
    def test_property_meta_access(self):
        '''
        Tests that property defined in meta Model is used on Model instance.
        '''
         
        