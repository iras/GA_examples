# Genetic algorithms examples - main.
# MIT License.


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import symmetric_travelling_salesman_ga as ga


REF_WORD = 'supercalifragilisticexpialidocious'


population  = ga.get_initial_population( 10, len( REF_WORD ) )
mating_pool = ga.selection( population, REF_WORD )


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


def data_gen( t = 0 ):
    global mating_pool
    while max( mating_pool.keys() ) < 1.0:
        population  = ga.reproduction( mating_pool, 10 );
        mating_pool = ga.selection( population, REF_WORD );
        #print max(mating_pool.keys())
        t += 1



        xpairs = []
        ypairs = []
        for i in range(100):
            xpairs.append( list( 10 + np.random.randn( 2 ) + 10 ) )
            ypairs.append( list( 10 + np.random.randn( 2 ) + 10 ) )
        xlist = []
        ylist = []
        for xends, yends in zip( xpairs, ypairs ):
            xlist.extend( xends )
            xlist.append( None )
            ylist.extend( yends )
            ylist.append( None )



        yield t, max( mating_pool.keys() ), [xlist, ylist]


def init():
    ax0.set_ylim( 0, 1.0 )
    ax0.set_xlim( 0, 100 )
    del xdata[:]
    del ydata[:]
    line[0].set_data( xdata, ydata )

    ax1.set_ylim( 0, 40 )
    ax1.set_xlim( 0, 40 )
    global background
    background = ax1.figure.canvas.copy_from_bbox( ax1.bbox )
    return line


def run( data ):
    t, y, list_lines = data

    # update data top plot.
    xdata.append( t )
    ydata.append( y )
    xmin, xmax = ax0.get_xlim()

    if y == 1.0:
        animation.event_source.stop()
        plt.axvline(x=t, color='red', lw=.5, ls='-.')   # visible if blit=False
        
        print(
            "\n - search word converged at step %s. Please close matplotlib's window to end." % t
        )

    if t >= xmax:
        ax0.set_xlim( xmin, 1.5*xmax )
        ax0.figure.canvas.draw()
        ax1.clear()
        ax1.set_ylim( 10, 30 )
        ax1.set_xlim( 10, 30 )
        ax1.figure.canvas.draw()

    line[0].set_data( xdata, ydata )

    # update data bottom plot - use blitter to make it fast.
    ax1.figure.canvas.restore_region( background )
    ax1.set_ylim( 10, 30 )
    ax1.set_xlim( 10, 30 )
    pict, = ax1.plot( list_lines[0], list_lines[1], 'b-' )
    ax1.draw_artist( pict )
    ax1.figure.canvas.blit( ax1.bbox )

    return line


animation = anim.FuncAnimation(
    fig, run, data_gen,
    blit=True, interval=0, repeat=False, init_func=init
)

#plt.tight_layout()
plt.show()
