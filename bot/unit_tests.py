# encoding=utf8
import unittest
import bot_parser


class MyTest(unittest.TestCase):

    def test_build_string(self):
        self.assertEqual(bot_parser.build_string("via carlo"), "CARLO")
        self.assertEqual(bot_parser.build_string("via carlò"), "CARLò")
        self.assertEqual(bot_parser.build_string("via"), "VIA")
        self.assertEqual(bot_parser.build_string("123"), "123")

    def test_remove_accents(self):
        self.assertEqual(
            bot_parser.remove_accents(
                "aaa".decode('ascii')), "aaa'")
        self.assertEqual(
            bot_parser.remove_accents(
                "123".decode('ascii')), "123'")


if __name__ == '__main__':
    unittest.main()
