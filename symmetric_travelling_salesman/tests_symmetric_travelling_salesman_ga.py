# Genetic algorithms examples - tests.
# MIT License.


import unittest
import os, sys
from io import StringIO
import numpy as np
from symmetric_travelling_salesman_ga import get_two_fittest_individuals, \
    selection


class TestSymmetricTSPGA( unittest.TestCase ):

    def test_get_two_fittest_individuals( self ):
        mating_pool = {
            76.536923: [
                [2, 0, 4, 1, 3, 5]
            ],
            74.07044: [
                [4, 0, 2, 5, 1, 3]
            ],
            87.66713: [
                [3, 2, 4, 5, 1, 0]
            ],
            74.588527: [
                [1, 0, 4, 3, 2, 5],
                [4, 0, 1, 5, 2, 3]
            ],
            80.016984: [
                [4, 0, 1, 3, 2, 5]
            ],
            80.786677: [
                [2, 3, 5, 0, 4, 1]
            ],
            99.714759: [
                [4, 2, 3, 0, 5, 1]
            ],
            81.907491: [
                [2, 5, 3, 0, 1, 4]
            ],
            67.960835: [
                [0, 2, 5, 4, 3, 1]
            ]
        }

        self.assertEqual(
            sorted( get_two_fittest_individuals( mating_pool ) ),
            sorted( [[0, 2, 5, 4, 3, 1], [4, 0, 2, 5, 1, 3]] )
        )


    def test_selection( self ):

        population = [
            [3, 4, 0, 5, 2, 1],
            [4, 0, 5, 3, 1, 2],
            [2, 3, 5, 4, 1, 0],
            [0, 5, 4, 3, 2, 1],
            [3, 1, 5, 4, 0, 2],
            [4, 0, 5, 2, 1, 3],
            [0, 5, 2, 4, 3, 1],
            [2, 0, 3, 1, 5, 4],
            [4, 1, 0, 3, 2, 5],
            [2, 1, 4, 5, 3, 0]
        ]
        dist_memo = {}
        city_dict = {
            0: np.array([19.19093807,  2.91402521]),
            1: np.array([14.85198645, 15.44710273]),
            2: np.array([ 4.493833 , 14.9924073]),
            3: np.array([11.60715415, 13.73150432]),
            4: np.array([9.01391852, 0.20177464]),
            5: np.array([16.76969068, 17.55312157])
        }

        length, dist_memo_1, mating_pool = selection(
            population,
            dist_memo,
            city_dict
        )

        flag_length = (length == 84.356504)
        flag_dist_memo_1 = (dist_memo_1 == {
            (3, 4): 13.776010171547291,
            (0, 4): 10.532237657570567,
            (0, 5): 14.837977664120775,
            (2, 5): 12.540093275259023,
            (1, 2): 10.368128607796578,
            (1, 3): 3.670451547087608,
            (3, 5): 6.423125549845806,
            (2, 4): 15.465897568236134,
            (2, 3): 7.224210275733271,
            (4, 5): 19.005821268312808,
            (1, 4): 16.324921614728737,
            (0, 1): 13.2629006360988,
            (0, 2): 19.023464756732736,
            (1, 5): 2.8483161461106867,
            (0, 3): 13.211042080038085
        } )
        flag_mating_pool = ( mating_pool == {
            65.724899: [[3, 4, 0, 5, 2, 1], [4, 0, 5, 2, 1, 3]],
            61.297819: [[4, 0, 5, 3, 1, 2]],
            81.264444: [[2, 3, 5, 4, 1, 0]],
            78.475049: [[0, 5, 4, 3, 2, 1]],
            62.304502: [[3, 1, 5, 4, 0, 2]],
            73.553331: [[0, 5, 2, 4, 3, 1]],
            73.224993: [[2, 0, 3, 1, 5, 4]],
            81.568989: [[4, 1, 0, 3, 2, 5]],\
            84.356504: [[2, 1, 4, 5, 3, 0]]
        } )

        self.assertTrue( flag_length and flag_dist_memo_1 and flag_mating_pool )


if __name__ == '__main__':
    unittest.main()
