import unittest
from app import *

class TestModule(unittest.TestCase):

    def testInputs(self):
        '''function should fail on wrong type inputs'''
        self.assertRaisesRegex(TypeError, 'Expected User input', user_needs_avatar, 'asd')
        self.assertRaisesRegex(TypeError, 'Expected string input', get_updates_on_avatar, '1', 2)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_updates_on_avatar, 17, 2)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_avatar_for_a_user, 1 )
        self.assertRaisesRegex(TypeError, 'Expected string input', get_music_sheets_by_a_user, 1)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_music_sheets_by_a_user, [1, 2])
        self.assertRaisesRegex(TypeError, 'Expected string input', get_inbox_messages_for_user, 1)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_inbox_messages_for_user, {"one":1})
        self.assertRaisesRegex(TypeError, 'Expected string input', get_music_sheets_letter, 1)
        self.assertRaisesRegex(TypeError, 'Expected string input', get_artists_letter, 1)
        self.assertRaisesRegex(ValueError, 'String is too long', get_music_sheets_letter, "as")
        self.assertRaisesRegex(ValueError, 'String is too long', get_artists_letter, "as")
        self.assertRaisesRegex(TypeError, 'Expected string input', get_music_sheets_for_genre, 1)

if "__name__" == "__main__":
    unittest.main()