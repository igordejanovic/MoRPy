import unittest

class MoRPTest(unittest.TestCase):
    
    def test_get_MoRP(self):
        '''
        Tests MoRP instantiation.
        '''
        
        from morpy import repository
        
        print repository.morp.inner_models
        
        