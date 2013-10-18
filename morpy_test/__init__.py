import unittest

class MoRPTest(unittest.TestCase):
    
    def test_get_MoRP(self):
        '''
        Tests MoRP instantiation.
        '''
        
        from morpy import repository
        
        morp = repository.get_MoRP()
        
        print morp.child_models
        
        