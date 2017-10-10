import os
import time
import unittest

from ddt import ddt, data
from freezegun import freeze_time
from six import u

from timestring import parse
from timestring.text2num import text2num
from timestring.timestring_re import TIMESTRING_RE as ts


@freeze_time('2017-06-16 19:37:22')
@ddt
class T(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse('tuesday at 10pm')['hour'], 22)
        self.assertEqual(parse('tuesday at 10pm')['weekday'], 2)
        self.assertEqual(parse('may of 2014')['year'], 2014)

    @data((1, 'one'),
          (12, 'twelve'),
          (72, 'seventy two'),
          (300, 'three hundred'),
          (1200, 'twelve hundred'),
          (12304, 'twelve thousand three hundred four'),
          (6000000, 'six million'),
          (6400005, 'six million four hundred thousand five'),
          (123456789012,
           'one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve'),
          (4000000000000000000000000000000000, 'four decillion'))
    def test_string_to_number(self, data):
        (equals, string) = data
        self.assertEqual(text2num(string), equals)
        self.assertEqual(text2num(u(string)), equals)

    def test_word_boundaries(self):
        res = ts.search('next mon')
        self.assertNotEqual(res, None)
        res = ts.search('santa monica')
        self.assertEqual(res, None)
        res = ts.search('tuesday two weeks ago')
        self.assertNotEqual(res, None)
        res = ts.search('fri')
        self.assertNotEqual(res, None)
        res = ts.search('dec')
        self.assertNotEqual(res, None)
        res = ts.search('Current weather in East hanover new jersey')
        self.assertEqual(res, None)
        res = ts.search('august')
        self.assertNotEqual(res, None)
        res = ts.search('23rd feb 9:35pm')
        self.assertNotEqual(res, None)


def main():
    os.environ['TZ'] = 'UTC'
    time.tzset()
    unittest.main()


if __name__ == '__main__':
    main()
