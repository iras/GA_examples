# Genetic algorithms examples - GA algorithm.
# MIT License.


from datetime import datetime
import numpy as np
import random
import time
from pprint import pprint as pp


random.seed( time.time() )


def get_initial_population( population_size, city_ids ):
    # get population of possible routes.
    # A route is defined as a list of cities explored in increasing order.
    # NB: City(0) to city(1) to city(2) to... city(n) to city(0).
    population = []
    for n in range( population_size ):
        route = list( city_ids )  # copy list. The copy will be shuffled below.
        np.random.shuffle( route )
        population.append( route )
    return population


def get_fitness_score( route, dist_memo, city_dict ):

    # NB: the fitness score here is the length of the path through all cities
    #     including the last city and the first city to complete the round trip.

    # append the first city to complete the route's round trip.
    route_copy = list( route )  # copy list since it'll be changed.
    route_copy.append( route_copy[0] )

    length = 0
    prev_city_id = route_copy[0]
    for city_id in route_copy[1:]:
        index = ( min(prev_city_id, city_id), max(prev_city_id, city_id), )
        # add distance between those two cities if not already memoised.
        if index not in dist_memo:
            dist_memo[ index ] = np.linalg.norm(
                city_dict[ city_id ] - city_dict[ prev_city_id ]
            )
        length += dist_memo[ index ]
        prev_city_id = city_id

    return round(length, 6), dist_memo


def crossover( two_fittest_individuals ):

    route_1, route_2 = two_fittest_individuals
    route_1 = list( route_1 )  # copy it since the copy might be altered below.

    # This TSP breeding step uses the "ordered crossover" method explained by
    # Lee Jacobson (2012) in: www.theprojectspot.com/tutorial-post/applying-a
    #                 -genetic-algorithm-to-the-travelling-salesman-problem/5

    len_route_1 = len( route_1 )

    ### route_1's gene is a contiguous sublist of route_1.
    route_1_gene_length = int( len_route_1 / 2 )
    route_1_gene_start  = np.random.randint( len_route_1 )
    route_1_gene_end    = route_1_gene_start + route_1_gene_length
    # double up route_1 to avoid the gene being at the two extremes of the list.
    if route_1_gene_end > len_route_1:
        route_1.extend( route_1 )
    # extract route_1's gene.
    route_1_gene = route_1[ route_1_gene_start : route_1_gene_end ]

    ### route_2's gene is a contiguous sublist of route_2.
    route_2_gene = list( route_2 )  # initially set it as a copy of route_2 and
    # then remove cities in route_2_gene that are already in route_1_gene.
    # The deletion of specific ids will preserve the route_2's items order.
    for city_id in route_1_gene:
        del route_2_gene[ route_2_gene.index( city_id ) ]

    ### child_route.
    child_route = route_1_gene + route_2_gene
    assert( len( child_route ) == len( route_2 ) )

    return np.array( child_route )


def get_mutated_route( route, number_of_mutations ):

    for _ in range( number_of_mutations ):
        # swap two random cities in the given route.
        list_id_0, list_id_1 = np.random.choice( range( len(route) ), 2 )
        city_0 = route[ list_id_0 ]
        city_1 = route[ list_id_1 ]
        route[ list_id_0 ] = city_1
        route[ list_id_1 ] = city_0
    return route


def selection( population, dist_memo, city_dict ):

    # build mating pool with fitness scores as keys.
    mating_pool = {}
    for route in population:
        length, dist_memo = get_fitness_score( route, dist_memo, city_dict )
        if length not in mating_pool.keys():
            mating_pool[ length ] = []
        mating_pool[ length ].append( route )

    return length, dist_memo, mating_pool


def get_normalised_fitness_score_mating_pool( mating_pool ):
    # normalise mating_pool's fitness score values.
    # i.e.  from:  fitness-score key. e.g.: [ 0.428571, 0.142857, 1e-05 ]
    #        to:   normalised fs key. e.g.: [ 0.749986, 0.249995, 1.75e-05 ]
    #
    mating_pool_copy = dict( mating_pool )  # copy dict.
    # replace fitness score 0.0 with a very low non-zero value.
    if 0.0 in mating_pool_copy.keys():
        mating_pool_copy[ 0.00001 ] = mating_pool_copy.pop( 0.0 )
    # calculate scaling_factor.
    scaling_factor = 1.0 / sum( mating_pool_copy.keys() )
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
        two_fittest_individuals.append( list_associated_to_the_max_key[ 0 ] )
        # get the second fittest individual.
        list_associated_to_the_second_max_key = \
            nfs_mating_pool.pop( max( nfs_mating_pool.keys() ) )
        two_fittest_individuals.append(
            random.sample( list_associated_to_the_second_max_key, 1 )[0]
        )
    return two_fittest_individuals


def reproduction( mating_pool, length_new_population ):

    normalised_fitness_score_mating_pool = \
        get_normalised_fitness_score_mating_pool( mating_pool )
    two_fittest_individuals = get_two_fittest_individuals(
        normalised_fitness_score_mating_pool
    )

    # mating.
    #
    new_population = []
    for i in range( length_new_population ):

        child_route = crossover( two_fittest_individuals )
        child_route = get_mutated_route( child_route, 1 )
        new_population.append( child_route )

    return new_population
