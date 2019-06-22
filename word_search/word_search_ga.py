# Genetic algorithms examples - GA algorithm.
# MIT License.


from datetime import datetime
import numpy as np
import random
import time


random.seed( time.time() )


def get_initial_population( population_size, word_length ):

    population = []
    for n in range( population_size ):
        population.append(
            ''.join(
                [ chr( random.randint( 97, 122 ) ) for m in range(word_length) ]
            )
        )
    return population


def get_fitness_score( word, ref ):

    assert( len( word ) == len( ref ) )

    charwise_comparisons = [ float(word[n]==ref[n]) for n in range(len(word)) ]
    return sum( charwise_comparisons ) / float( len( ref ) )


def crossover( two_fittest_individuals ):

    word_1, word_2 = two_fittest_individuals
    assert( len( word_1 ) == len( word_2 ) )

    # random-points crossover. This seems to be comparatively the fastest.
    # choose half random cells from word_1 and replace them with word_2's cells.
    number_letter_substitutions = int( len(word_1) / 2.0 )
    random_positions = random.sample(  # e.g.: [ 1, 4, 6, 7 ]
        range( len( word_1 ) ),        # e.g.: [ 0, 1, 2, 3, 4, 5, 6, 7 ]
        number_letter_substitutions    # e.g.: 4
    )
    tuples = zip( word_1, word_2 )

    return ''.join(
        [ t[0] if i in random_positions else t[1] for i, t in enumerate(tuples) ]
    )

    """
    # mixed crossover.
    crossing_mode = random.random()
    if crossing_mode > 0.666:

        # single-point crossover.
        half = int( len( word_1 ) / 2.0 )
        return word_1[:half] + word_2[half:]

    elif crossing_mode > 0.5:
        # uniform crossover (even numbers).
        return ''.join(
            [ t[0] if i%2 else t[1] for i, t in enumerate(zip(word_1, word_2)) ]
        )

    else:
        # uniform crossover (odd numbers).
        return ''.join(
            [ t[1] if i%2 else t[0] for i, t in enumerate(zip(word_1, word_2)) ]
        )
    """


def get_mutated_word( word, number_of_mutations ):

    non_overlapping_random_places_in_the_word = \
        random.sample( range(0, len(word)), number_of_mutations )

    # inject mutations in those places.
    word_as_list = list( word )
    for n in non_overlapping_random_places_in_the_word:
        word_as_list[n] = chr( random.randint(97, 122) )

    return ''.join( word_as_list )


def selection( population, ref ):

    # build mating pool with fitness scores as keys.
    mating_pool = {}
    for word in population:
        score = get_fitness_score( word, ref )
        if score not in mating_pool.keys():
            mating_pool[ score ] = []
        mating_pool[ score ].append( word )

    return mating_pool


def get_normalised_fitness_score_mating_pool( mating_pool ):
    # normalise mating_pool's fitness score values.
    # i.e.  from:  fitness-score key. e.g.: [ 0.428571, 0.142857, 1e-05 ]
    #        to:   normalised fs key. e.g.: [0.749986, 0.249995, 1.75e-05]
    #
    mating_pool_copy = dict( mating_pool )  # copy dict.
    # replace fitness score 0.0 with a very low non-zero value.
    if 0.0 in mating_pool_copy.keys():
        mating_pool_copy[ 0.00001 ] = mating_pool_copy.pop( 0.0 )
    # calculate scaling_factor.
    denominator_of_scaling_factor = 0
    for k in mating_pool_copy.keys():
        denominator_of_scaling_factor += k
    scaling_factor = 1.0 / denominator_of_scaling_factor
    # generate pool with normalised fitness score values.
    nfs_mating_pool = {}
    for k in mating_pool_copy.keys():
        nfs_mating_pool[ scaling_factor * k ] = mating_pool_copy[ k ]

    return nfs_mating_pool


def get_two_fittest_individuals( nfs_mating_pool ):
    # get the two fittest individuals.
    # Two individuals were chosen here to maximise genetic diversity although
    # more than 2 individuals could be used.
    #
    two_fittest_individuals = []
    list_associated_to_the_max_key = \
        nfs_mating_pool.pop( max( nfs_mating_pool.keys() ) )
    if len( list_associated_to_the_max_key ) > 1:
        # get two fittest individuals.
        two_fittest_individuals = random.sample(
            list_associated_to_the_max_key,
            2
        )
    else:
        # keep the single fittest individual.
        two_fittest_individuals.append(
            ''.join( list_associated_to_the_max_key[ 0 ] )
        )
        # get the second fittest individual.
        list_associated_to_the_new_max_key = \
            nfs_mating_pool.pop( max( nfs_mating_pool.keys() ) )
        two_fittest_individuals.append(
            ''.join( random.sample( list_associated_to_the_new_max_key, 1 ) )
        )

    return two_fittest_individuals


def reproduction( mating_pool, length_new_population ):

    two_fittest_individuals = get_two_fittest_individuals(
        get_normalised_fitness_score_mating_pool( mating_pool )
    )

    print( two_fittest_individuals )

    # mating.
    #
    new_population = []
    for i in range( length_new_population ):

        child_word = crossover( two_fittest_individuals )
        child_word = get_mutated_word( child_word, 1 )
        new_population.append( child_word )

    print( new_population )

    return new_population
