# Genetic algorithms examples - main.
# MIT License.


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import word_search_ga as ga


REF_WORD = 'supercalifragilisticexpialidocious'


population  = ga.get_initial_population( 10, len( REF_WORD ) )
mating_pool = ga.selection( population, REF_WORD )


def data_gen( t = 0 ):
    global mating_pool
    while max( mating_pool.keys() ) < 1.0:
        population = ga.reproduction( mating_pool, 10 );
        mating_pool = ga.selection( population, REF_WORD );
        #print max(mating_pool.keys())

        t += 1
        yield t, max( mating_pool.keys() )


def init():
    ax.set_ylim( 0, 1.0 )
    ax.set_xlim( 0, 100 )
    del xdata[:]
    del ydata[:]
    line.set_data( xdata, ydata )
    return line,


def run( data ):
    # update the data
    t, y = data
    xdata.append( t )
    ydata.append( y )
    xmin, xmax = ax.get_xlim()

    if y == 1.0:
        animation.event_source.stop()
        plt.axvline(x=t, color='red', lw=.5, ls='-.')   # visible if blit=False
        
        print(
            "\n - search word converged at step %s. \
             Please close matplotlib's window to end." % t
        )

    if t >= xmax:
        ax.set_xlim( xmin, 1.5*xmax )
        ax.figure.canvas.draw()
    line.set_data( xdata, ydata )

    return line,


fig, ax = plt.subplots()
line, = ax.plot( [], [], lw=.5 )
ax.grid()
xdata, ydata = [], []

animation = anim.FuncAnimation(
    fig, run, data_gen,
    blit=True, interval=1, repeat=False, init_func=init
)
#plt.tight_layout()
plt.ylabel("max fitness score")
plt.xlabel("time (steps)")
plt.show()
