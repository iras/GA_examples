# Genetic algorithms examples - main.
# MIT License.

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import symmetric_travelling_salesman_ga as ga


# Symmetric TSP.
#
#   "Given a list of cities and the distances between each pair of cities, what
#    is the shortest possible route that visits each city and returns to the
#    origin city?".


################################################################################


NUMBER_OF_CITIES = 30
twopi = 2 * np.pi
CITY_DICT = dict(
    zip(
        list( np.arange( NUMBER_OF_CITIES ) ),  # city ids.
        np.array( list(                         # list of tuples (2D positions).
            zip(
                [10+10*np.cos(i / NUMBER_OF_CITIES*twopi) for i in range( NUMBER_OF_CITIES )],
                [10+10*np.sin(i / NUMBER_OF_CITIES*twopi) for i in range( NUMBER_OF_CITIES )]
                #list( 20 * np.random.random(  NUMBER_OF_CITIES) ),
                #list( 20 * np.random.random(  NUMBER_OF_CITIES) )
            )
        ) )
    )
)
# e.g.: CITY_DICT = {
#          0: array([17.22729579,  7.81743567]),
#          1: array([ 2.18160281, 14.34073598]),
#          2: array([19.18576723,  3.90946777]),
#          ...
#       )

dist_memo = {}  # use memoization to avoid square roots' repeats.

# init symmetric TSP GA.
curr_shortest_distance = 1000
population = ga.get_initial_population( 10, list(CITY_DICT.keys()) )
length, dist_memo, mating_pool = ga.selection(
    population,
    dist_memo,
    CITY_DICT
)


#######  init UI  ##############################################################


def get_annotation():
    return plt.annotate( '', xy = ( 5, -5 ), color='green' )

xdata, ydata = [], []
fig, (ax0, ax1) = plt.subplots( 2, figsize=(4,15) )
line_0, = ax0.plot( [], [], lw=.5 )
line_1, = ax1.plot( [], [], lw=.5, color='r')
line = [ line_0, line_1 ]
# top plot.
ax0.grid()
ax0.set_ylabel( 'fitness score' )
ax0.set_xlabel( 'time (steps)' )
# bottom plot.
ax1.set_yticklabels( [] )
ax1.set_xticklabels( [] )
ax1.xaxis.set_ticks_position( 'none' )
ax1.yaxis.set_ticks_position( 'none' )
annotation = get_annotation()


################################################################################


def init():
    global annotation
    global background
    # init top plot.
    ax0.set_ylim( 0, 1000 )
    ax0.set_xlim( 0, 100 )
    del xdata[:]
    del ydata[:]
    line[0].set_data( xdata, ydata )
    # init bottom plot.
    ax1.clear()
    ax1.set_ylim( -10, 30 )
    ax1.set_xlim( -10, 30 )
    # add annotation and capture blank background.
    annotation = get_annotation()
    background = ax1.figure.canvas.copy_from_bbox( ax1.bbox )
    return line


def data_gen( t = 0 ):
    global mating_pool
    global population
    global curr_shortest_distance
    global dist_memo


    while max( mating_pool.keys() ) < 10000.0:

        # fittest items. 
        fittest_items_key = min( mating_pool.keys() )
        fittest_items_copy = list( mating_pool[ fittest_items_key ] )


        population = ga.reproduction( mating_pool, 10 );
        length, dist_memo, mating_pool = ga.selection(
            population,
            dist_memo,
            CITY_DICT
        )


        # elitarism step.
        if fittest_items_key not in mating_pool:
            mating_pool[ fittest_items_key ] = []
        mating_pool[ fittest_items_key ].extend( fittest_items_copy )





        if length < curr_shortest_distance:
            print( '•••  %s' % length )
            curr_shortest_distance = length
        t += 1

        min_dist_path_id = min( mating_pool.keys() )
        min_dist_path = list( mating_pool[ min_dist_path_id ][0] )
        min_dist_path.append( min_dist_path[0] )  # close the path.
        xpairs = []
        ypairs = []
        for i in range( len( min_dist_path ) - 1 ):
            x0, y0 = CITY_DICT[ min_dist_path[ i ] ]
            x1, y1 = CITY_DICT[ min_dist_path[ i + 1 ] ]
            xpairs.append( [ x0, x1 ] )
            ypairs.append( [ y0, y1 ] )
        # add last one connected with the first one.
        x0, y0 = CITY_DICT[ min_dist_path[ len( min_dist_path ) - 1 ] ]
        x1, y1 = CITY_DICT[ min_dist_path[ 0 ] ]
        xpairs.append( [ x0, x1 ] )
        ypairs.append( [ y0, y1 ] )
        # plot speed optimisation.
        xlist = []
        ylist = []
        for xends, yends in zip( xpairs, ypairs ):
            xlist.extend( xends )
            xlist.append( None )
            ylist.extend( yends )
            ylist.append( None )

        yield t, length, [xlist, ylist]


def run( data ):
    global fig
    global annotation
    global curr_shortest_distance
    t, y, list_lines = data

    # update data top plot.
    xdata.append( t )
    ydata.append( y )
    xmin, xmax = ax0.get_xlim()

    # extend horizontal axis.
    if t >= xmax:
        ax0.set_xlim( xmin, 2 * xmax )
        ax0.figure.canvas.draw()
        ax1.clear()
        ax1.set_ylim( -10, 30 )
        ax1.set_xlim( -10, 30 )
        annotation = get_annotation()
        ax1.figure.canvas.draw()

    # remove old ax1's lines and add new lines.
    try:
        ax1.lines.remove(ax1.lines[0])
    except:
        pass
    line[0].set_data( xdata, ydata )

    # update bottom plot - use blitter to make it fast.
    ax1.figure.canvas.restore_region( background )
    ax1.set_ylim( -10, 30 )
    ax1.set_xlim( -10, 30 )
    pict, = ax1.plot(
        list_lines[0],
        list_lines[1],
        'b-',
        linewidth=.5,
        color='blue',
        marker='o',
        markersize=3
    )
    ax1.draw_artist( pict )
    annotation.set_text( y )
    ax1.figure.canvas.blit( ax1.bbox )

    if y == curr_shortest_distance:
        fig.savefig(
            os.path.expanduser( '~/Desktop/screenshots/%s.png' % y ),
            dpi=150
        )

    return line


animation = anim.FuncAnimation(
    fig, run, data_gen,
    blit=True, interval=0, repeat=False, init_func=init
)

#plt.tight_layout()
plt.show()