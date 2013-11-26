import unittest
from morpy import repository
from morpy.const import NAMED_ELEMENT, MULTIPLICITY, MODEL, REFERENCE, PROPERTY,\
    PRIMITIVE_TYPES, PRIMITIVE_TYPES_PRIMITIVE_TYPE, PRIMITIVE_TYPES_BOOLEAN,\
    PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING, LANGUAGE, MOGRAM

morp_toplevel_model_names = [LANGUAGE, MOGRAM, NAMED_ELEMENT, MULTIPLICITY, MODEL, REFERENCE, PROPERTY, PRIMITIVE_TYPES]
primitive_type_models = [PRIMITIVE_TYPES_PRIMITIVE_TYPE, PRIMITIVE_TYPES_BOOLEAN, \
                         PRIMITIVE_TYPES_INTEGER, PRIMITIVE_TYPES_STRING]

class MoRPTest(unittest.TestCase):
    
    def test_MoRP_models(self):
        '''
        Tests MoRP models.
        '''
        
        # Top-level abstract models
        abstract_models = filter(lambda m: m.abstract, repository.morp.contents)
        abstract_model_names = [x.name for x in abstract_models]

        self.assertEqual(len(set(abstract_model_names).difference(set([NAMED_ELEMENT, MULTIPLICITY]))), 0)
        
        # Top-level models
        toplevel_model_names = [x.name for x in repository.morp.contents]
        self.assertEqual(len(set(toplevel_model_names).difference(morp_toplevel_model_names)), 0)
        
    def test_model_iteration(self):
        '''
        Test that model iteration returns inner models.
        '''
        
        for model in repository.morp:
            self.assertIn(model.name, morp_toplevel_model_names)
            if model.name == PRIMITIVE_TYPES:
                primitive_types = model
            
        for model in primitive_types:
            self.assertIn(model.name, primitive_type_models)

    def test_property_meta_access(self):
        '''
        Tests that property defined in meta Model is used on Model instance.
        '''
         
        