import unittest
from app import *

class TestModule(unittest.TestCase):

    def testInputs(self):
        '''function should fail on wrong type inputs'''
        self.assertRaisesRegex(TypeError, 'Expected User input', user_needs_avatar, 'asd')
        self.assertRaisesRegex(TypeError, 'Expected string input', get_updates_on_avatar, '1', 2)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_updates_on_avatar, 17, 2)

if "__name__" == "__main__":
    unittest.main()