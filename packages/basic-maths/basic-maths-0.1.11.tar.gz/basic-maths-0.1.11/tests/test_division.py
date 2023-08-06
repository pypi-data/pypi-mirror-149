import unittest
import math
from basic_division import Division


class DivisionTestCase(unittest.TestCase):

    def setUp(self):
        self.division = Division(2)

    def test_zero(self):
        """Test 0 divided by 2"""

        # 0 divided by 2 returns 0.0
        result = self.division.divide(0)
        self.assertEqual(result, 0.0)

    def test_divide_by_zero(self):
        """Test Int divided by 0"""

        self.division_by_zero = Division(0)
        with self.assertRaises(ZeroDivisionError):
            self.division_by_zero.divide(5)

    def test_natural_number(self):
        """Test natural number 5 divided by 2"""

        # 5 divided by 2 returns 2.5
        result = self.division.divide(5)
        self.assertEqual(result, 2.5)

    def test_integer_number(self):
        """Test integer number -14 divided by 2"""

        # -14 divided by 2 returns -7
        result = self.division.divide(-14)
        self.assertEqual(result, -7)

    def test_real_number(self):
        """Test real number PI divided by 2"""

        # PI divided by 2 returns 1.5707963267948966
        result = self.division.divide(math.pi)
        self.assertEqual(result, 1.5707963267948966)

    if __name__ == '__main__':
        unittest.main()
