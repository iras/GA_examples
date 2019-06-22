# Genetic algorithms examples - tests.
# MIT License.


import unittest
import os, sys
from io import StringIO
from word_search_ga import get_fitness_score, crossover, get_mutated_word, \
    get_normalised_fitness_score_mating_pool, get_two_fittest_individuals



class TestWordSearchGA( unittest.TestCase ):


    def test_get_fitness_score_1( self ):
        self.assertEqual( get_fitness_score( 'qwerty', 'queens'), 1/3.0 )


    def test_get_fitness_score_2( self ):
        with self.assertRaises( AssertionError ) as ctx:
            get_fitness_score( 'evolution', 'queens')
        # expected error thrown because of different lenghts of the input words.


    def test_crossover( self ):
        # random-points crossover test.
        # NB: This is just a probabilistic test and would need a better test or
        #     a new crossover function.
        #     A crossover word will be generated ten thousands times and the
        #     test will always need to be True.
        word_1 = 'abcdefgzy'
        word_2 = 'rstuvwxyz'
        number_letter_substitutions = int( len( word_1 ) / 2.0 )

        battery_test_list = []
        while len( battery_test_list ) < 10000:

            crossover_word = crossover( (word_1, word_2,) )

            crossover_word_1_count = sum([
                1 if crossover_word[i] in word_1 else 0
                for i in range( len( word_1 ) )
            ])

            crossover_word_2_count = sum([
                1 if crossover_word[i] in word_2 else 0
                for i in range( len( word_2 ) )
            ])

            battery_test_list.append(
                ( crossover_word_1_count >= number_letter_substitutions ) and \
                ( crossover_word_2_count >= number_letter_substitutions )
            )

        self.assertTrue( all( battery_test_list ) )


    def test_get_mutated_word( self ):
        # NB: This is just a probabilistic test and would need a better test or
        #     a new get_mutated_word function.
        #     This will be tested ten thousands times and the outcome will
        #     always need to be True.
        word = 'abcdefgzy'
        number_of_mutations = 1

        battery_test_list = []
        while len( battery_test_list ) < 10000:

            mutated_word = get_mutated_word( word, number_of_mutations )

            mutated_word_count = sum([
                1 if mutated_word[i] in word else 0
                for i in range( len( word ) )
            ])

            battery_test_list.append(
                ( mutated_word_count >= number_of_mutations )
            )

        self.assertTrue( all( battery_test_list ) )


    def test_get_normalised_fitness_score_mating_pool( self ):
        mating_pool = {
            0.0: [
                'vfwpcyze',
                'cqehqacd',
                'ikgqnnlz',
                'cpfplhcj',
                'qwzjpbtk',
                'ivluyiew',
                'gsnbcici',
                'mqdkpvgn',
            ],
            0.125: ['svvdlsof', 'ebjvywaz']
        }
        nfs_mating_pool = {
            7.999360051195904e-05: [
                'vfwpcyze',
                'cqehqacd',
                'ikgqnnlz',
                'cpfplhcj',
                'qwzjpbtk',
                'ivluyiew',
                'gsnbcici',
                'mqdkpvgn',
            ],
            0.999920006399488: ['svvdlsof', 'ebjvywaz']
        }

        self.assertEqual(
            get_normalised_fitness_score_mating_pool( mating_pool ),
            nfs_mating_pool
        )


    def test_get_two_fittest_individuals( self ):
        nfs_mating_pool = {
            7.999360051195904e-05: [
                'vfwpcyze',
                'cqehqacd',
                'ikgqnnlz',
                'cpfplhcj',
                'qwzjpbtk',
                'ivluyiew',
                'gsnbcici',
                'mqdkpvgn',
            ],
            0.999920006399488: ['svvdlsof', 'ebjvywaz']
        }

        self.assertEqual(
            sorted( get_two_fittest_individuals( nfs_mating_pool ) ),
            sorted( ['svvdlsof', 'ebjvywaz'] )
        )



if __name__ == '__main__':
    unittest.main()
