#-*- coding: utf-8 -*-
###############################################################################
# Name: test_repository.py
# Purpose: Testing MoRP repository.
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2013 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
###############################################################################

import unittest
from morpy import Workspace
from morpy.const import NAMED_ELEMENT, MULTIPLICITY, MODEL, REFERENCE, \
    PROPERTY, PRIMITIVE_TYPES, PRIMITIVE_TYPES_PRIMITIVE_TYPE, \
    PRIMITIVE_TYPES_BOOLEAN, PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING,\
    LANGUAGE, MOGRAM, UUID_MODEL, UUID_PROPERTY, UUID_REFERENCE

morp_toplevel_model_names = [LANGUAGE, MOGRAM, NAMED_ELEMENT, MULTIPLICITY,\
    MODEL, REFERENCE, PROPERTY, PRIMITIVE_TYPES]
primitive_type_models = [PRIMITIVE_TYPES_PRIMITIVE_TYPE, \
    PRIMITIVE_TYPES_BOOLEAN, PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING]


class MoRPTest(unittest.TestCase):

    def test_MoRPRepository_is_singleton(self):

        self.assertTrue(Workspace() is Workspace())

    def test_find_by_uuid(self):
        '''
        Find MoRP object in repository by its UUID.
        '''
        self.assertEqual(Workspace().get_by_uuid(UUID_MODEL),
                         Workspace().model)
        self.assertEqual(Workspace().get_by_uuid(UUID_PROPERTY),
                         Workspace().prop)
        self.assertEqual(Workspace().get_by_uuid(UUID_REFERENCE),
                         Workspace().reference)
