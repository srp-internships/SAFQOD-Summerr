from user import calc
from django.test import SimpleTestCase


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        """"
        tests adding numbers
        """
        res = calc.add(10, 4)

        self.assertEqual(res, 14)
