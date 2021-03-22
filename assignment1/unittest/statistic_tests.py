import unittest

from assignment1 import statistic as stat

"""
The numbers for the test were calculated with Excel
"""

class MyTestCase(unittest.TestCase):

    def test_computeMeanRating(self):
        data = stat.computeMeanRating("ratings.csv")
        print(data)
        arith_means = data[0]
        median = data[1]
        mode = data[2]

        # Arithmetic means
        self.assertEqual(arith_means, 3.50156)
        # median
        self.assertEqual(median, 3.5)
        #mode
        self.assertEqual(mode, 4)



if __name__ == '__main__':
    unittest.main()
